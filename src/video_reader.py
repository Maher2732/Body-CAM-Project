from pathlib import Path
import subprocess
import json

from Data_Read import read_data


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
        print(f"Skipping existing clip: {output_path.name}\n")
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

    subprocess.run(command,check=True)


def main():
    
    df = read_data()

    segments=df[["video ID","timeframe"]].dropna()
    segments=segments.drop_duplicates()
    errors=[]
    for _,row in segments.iloc[5:].iterrows():
        video_id=row["video ID"]
        timeframe=row["timeframe"]
        
        try:
            start,end=parse_timeframe(timeframe)
            
            print(f"Extracting{video_id}: {timeframe}\n")
            
            extract_clip(video_id, start, end)
        except Exception as error:
            errors.append({
                "video_id":video_id,
                "timeframe":timeframe,
                "error":str(error)
            })
            print(f"Skipping {video_id}: {timeframe}")
        print("\nFinished processing clips.")

    if errors:
        print(f"\nErrors found: {len(errors)}")

        for error in errors:
            print(
                f"{error['video_id']} | "
                f"{error['timeframe']} | "
                f"{error['error']}"
            )
    else:
        print("No errors found.")

if __name__ == "__main__":
    main()