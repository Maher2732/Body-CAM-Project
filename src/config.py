import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"

PATH_KEYS = ["excel_path", "video_folder", "clip_folder", "cleaned_dataset"]


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"{CONFIG_PATH} not found. Copy config.example.json to "
            "config.json and fill in your values (see SETUP_INSTRUCTIONS.txt)."
        )

    with open(CONFIG_PATH, "r") as file:
        loaded = json.load(file)

   
    for key in PATH_KEYS:
        if key in loaded:
            loaded[key] = str(PROJECT_ROOT / loaded[key])

    return loaded


config = load_config()
