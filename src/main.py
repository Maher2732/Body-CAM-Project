import argparse
import subprocess

from config import config
from data_read import download_videos, get_urls, read_data
from dataset_builder import build_dataset, check_missing_clips, save_dataset
from explore import explore_data
from train_baseline import train_model
from video_reader import extract_clip, parse_timeframe


def extract_all_clips(df):
    segments = df[["video ID", "timeframe"]].dropna().drop_duplicates()

    errors = []

    for _, row in segments.iterrows():
        video_id = row["video ID"]
        timeframe = row["timeframe"]

        try:
            start, end = parse_timeframe(timeframe)

            print(f"Extracting {video_id}: {timeframe}")

            extract_clip(video_id, start, end)

        except (ValueError, subprocess.CalledProcessError) as error:
            errors.append(
                {
                    "video_id": video_id,
                    "timeframe": timeframe,
                    "error": str(error),
                }
            )

    return errors


def report_errors(errors):
    print("\nProcessing finished.")

    if not errors:
        print("No errors found.")
        return

    print(f"\nErrors found: {len(errors)}")

    for error in errors:
        print(f"{error['video_id']} | {error['timeframe']} | {error['error']}")


def report_missing_clips(df):
    missing_clips = check_missing_clips(df, config["clip_folder"])

    if not missing_clips:
        print("\nAll clips found in cleaned dataset.")
        return

    print(f"\nMissing clips after dataset build: {len(missing_clips)}")

    for clip in missing_clips:
        print(clip)


def parse_args():
    parser = argparse.ArgumentParser(description="Body camera risk analysis pipeline")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="don't download videos from YouTube (use the ones already in data/videos)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    raw_df = read_data(config["excel_path"])

    print(f"Rows: {raw_df.shape[0]}")
    print(f"Columns: {raw_df.shape[1]}")

    cleaned_df = build_dataset(raw_df)

    if not args.skip_download:
        download_videos(get_urls(raw_df))

    errors = extract_all_clips(cleaned_df)
    report_errors(errors)

    report_missing_clips(cleaned_df)

    save_dataset(cleaned_df, config["cleaned_dataset"])

    explore_data(cleaned_df)
    train_model(cleaned_df)


if __name__ == "__main__":
    main()
