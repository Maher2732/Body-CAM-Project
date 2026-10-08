import pandas as pd
import yt_dlp
import json
with open("config.json", "r") as file:
    config = json.load(file)


def read_data():
    df = pd.read_excel(config["excel_path"])

    df.columns = df.columns.str.strip()

    return df

def get_urls(df):
    cols_to_clean = [
        "gender",
        "race",
        "call for backup",
        "Unnamed: 39",
        "Unnamed: 40",
        "Unnamed: 41"
    ]

    for col in cols_to_clean:
        df[col] = df[col].astype("string").str.lower()

    urls = df[["video ID", "link"]].dropna()

    urls = urls[urls["link"].str.startswith("http")]

    urls = urls.drop_duplicates(subset=["video ID"])

    return urls
   


def download_videos(urls):
    for _, row in urls.iterrows():
        clip_id = row["video ID"]
        url = row["link"]
        options = {
            "outtmpl": f"{config["video_folder"]}/{clip_id}.%(ext)s",
            
            "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            
            "merge_output_format": "mp4",
            
            "noplaylist": True,
            
            "ignoreerrors": True,
            
            "quiet": False,
            
            "overwrites": False,
            
            "cookiesfrombrowser": ("firefox",)
            }
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                print(f"Downloading {clip_id}: {url}")
                ydl.download([url])
            except yt_dlp.utils.DownloadError as error:
                print(f"SKIPPING VIDEO: {url}")
                print(f"Reason: {error}")
