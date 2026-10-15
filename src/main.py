from data_read import read_data, get_urls, download_videos
from video_reader import parse_timeframe, extract_clip
from dataset_builder import (
    build_dataset,
    check_missing_clips,
    save_dataset
)
from explore import explore_data
from train_baseline import train_model
from config import config


def main():
    df = read_data(config["excel_path"])

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    urls = get_urls(df)
    download_videos(urls)

    segments = df[["video ID", "timeframe"]].dropna()
    segments = segments.drop_duplicates()

    errors = []

    for _, row in segments.iterrows():
        video_id = row["video ID"]
        timeframe = row["timeframe"]

        try:
            start, end = parse_timeframe(timeframe)

            print(f"Extracting {video_id}: {timeframe}")

            extract_clip(video_id, start, end)

        except Exception as error:
            errors.append({
                "video_id": video_id,
                "timeframe": timeframe,
                "error": str(error)
            })

    print("\nProcessing finished.")

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

    cleaned_df = build_dataset(df)

    missing_clips = check_missing_clips(
        cleaned_df,
        config["clip_folder"]
    )

    if missing_clips:
        print(f"\nMissing clips after dataset build: {len(missing_clips)}")

        for clip in missing_clips:
            print(clip)
    else:
        print("\nAll clips found in cleaned dataset.")

    save_dataset(
        cleaned_df,
        config["cleaned_dataset"]
    )

    explore_data(cleaned_df)
    train_model(cleaned_df)

if __name__ == "__main__":
    main()