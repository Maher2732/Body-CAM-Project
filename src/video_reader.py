from pathlib import Path
import subprocess
import json


with open("config.json", "r") as file:
    config = json.load(file)


VIDEO_FOLDER = Path(config["video_folder"])
CLIP_FOLDER = Path(config["clip_folder"])
FFMPEG_EXE = config["ffmpeg_exe"]


def parse_timeframe(timeframe):
    timeframe = timeframe.strip()

    timeframe = timeframe.replace("time:", "")
    timeframe = timeframe.replace("time", "")

    start, end = timeframe.split("-")

    start_min, start_sec = start.split(":")
    end_min, end_sec = end.split(":")

    start_seconds = int(start_min) * 60 + int(start_sec)
    end_seconds = int(end_min) * 60 + int(end_sec)

    return start_seconds, end_seconds


def extract_clip(video_id, start, end):
    input_path = VIDEO_FOLDER / f"{video_id}.mp4"

    CLIP_FOLDER.mkdir(parents=True, exist_ok=True)

    output_path = CLIP_FOLDER / f"{video_id}_{start}_{end}.mp4"

    if output_path.exists():
        print(f"Skipping existing clip: {output_path.name}")
        return

    duration = end - start

    command = [
        FFMPEG_EXE,
        "-ss", str(start),
        "-i", str(input_path),
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        str(output_path)
    ]

    subprocess.run(command, check=True)