from Data_Read import read_data, get_urls, download_videos
from video_reader import parse_timeframe, extract_clip


def main():
    
    df = read_data()

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


if __name__ == "__main__":
    main()