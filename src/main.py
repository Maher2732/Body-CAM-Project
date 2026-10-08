from Data_Read import read_data, get_urls, download_videos


def main():
    df = read_data()

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(df.columns.tolist())

    urls = get_urls(df)

    download_videos(urls)


if __name__ == "__main__":
    main()