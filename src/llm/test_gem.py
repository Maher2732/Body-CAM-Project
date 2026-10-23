import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import PROJECT_ROOT, config
from data_read import read_data
from llm.prompt import ANNOTATION_COLUMNS, build_prompt

MODEL = "gemini-3.1-flash-lite"
LIMIT = 3 
PAUSE_SECONDS = 5  # stay under the free tier's requests-per-minute limit
OUTPUT_FILE = PROJECT_ROOT / "results" / "predictions" / "gemini_flash_lite.json"

load_dotenv()

df = read_data(config["cleaned_dataset"])
client = genai.Client()
clips = df["clip_file"].unique()[:LIMIT]  # distinct clip names

prompt = build_prompt(ANNOTATION_COLUMNS)

results = {}
if OUTPUT_FILE.exists():
    results = json.loads(OUTPUT_FILE.read_text())

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

for clip in clips:
    if clip in results and "error" not in results[clip]:
        print(f"Skipping {clip} (already done)")
        continue

    print(f"Labelling {clip}")

    try:
        video = client.files.upload(file=str(Path(config["clip_folder"]) / clip))

        while video.state.name == "PROCESSING":
            time.sleep(2)
            video = client.files.get(name=video.name)

        response = client.models.generate_content(
            model=MODEL,
            contents=[video, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0,
            ),
        )
        results[clip] = json.loads(response.text)

        # Don't leave body-cam footage on Google's servers longer than needed
        client.files.delete(name=video.name)

    except Exception as error:
        print(f"  FAILED: {error}")
        results[clip] = {"error": str(error)}

    OUTPUT_FILE.write_text(json.dumps(results, indent=2))

    time.sleep(PAUSE_SECONDS)

done = sum("error" not in answer for answer in results.values())
print(f"\nDone: {done} clips labelled, {len(results) - done} failed -> {OUTPUT_FILE}")
