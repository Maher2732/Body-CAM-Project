from pathlib import Path
import pandas as pd
from video_reader import parse_timeframe


COLUMN_RENAMES = {
    "Unnamed: 11": "conflict_escalation_gesture",
    "Unnamed: 12": "conflict_escalation_gesture_impact",
    "Unnamed: 13": "face visible",
    "Unnamed: 17": "facial expression type",
    "Unnamed: 18": "facial expression impact",
    "Unnamed: 19": "facial escalation cause impact",
    "Unnamed: 20": "impact resulting from facial escalation",
    "Unnamed: 27": "escalation causing voice and speech patterns",
    "Unnamed: 28": "impact resulting from voice and speech patterns",
    "Unnamed: 29": "escalation sentence",
    "Unnamed: 34": "officer experience",
    "Unnamed: 39": "audit or normal",
    "Unnamed: 40": "person injured",
    "Unnamed: 41": "dead or unconscious",
    "Unnamed: 42": "has the person died",
}


NUMERIC_COLUMNS = [
    "fighting stance",
    "sudden movement",
    "conflict escalation gesture",
    "conflict_escalation_gesture_impact",
    "conflict escation facial",
    "facial expression impact",
    "impact resulting from facial escalation",
    "facial aggression",
    "stress",
    "lying",
    "conflict escalation voice",
    "impact resulting from voice and speech patterns",
    "hostility level speech",
    "distress level",
    "risk level",
]


TEXT_COLUMNS = [
    "source",
    "person",
    "activity",
    "weapon",
    "gesture",
    "face visible",
    "facial expression",
    "emotion",
    "facial expression type",
    "facial escalation cause impact",
    "ifspeaking",
    "voice tone",
    "escalation causing voice and speech patterns",
    "location",
    "type of instance",
    "gender",
    "race",
    "call for backup",
    "audit or normal",
    "person injured",
    "dead or unconscious",
]


def clean_columns(df):
    df = df.rename(columns=COLUMN_RENAMES)

    df = df.iloc[1:].reset_index(drop=True)

    return df


def clean_numeric_columns(df):
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df


def clean_text_columns(df):
    for col in TEXT_COLUMNS:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    return df


def add_clip_files(df):
    df["clip_file"] = None

    for index, row in df.iterrows():
        video_id = row["video ID"]
        timeframe = row["timeframe"]

        start, end = parse_timeframe(timeframe)

        df.at[index, "clip_file"] = (
            f"{video_id}_{start}_{end}.mp4"
        )

    return df


def check_missing_clips(df, clip_folder):
    clip_folder = Path(clip_folder)

    missing_clips = []

    for _, row in df.iterrows():
        clip_path = (
            clip_folder /
            row["clip_file"]
        )

        if not clip_path.exists():
            missing_clips.append(
                row["clip_file"]
            )

    return missing_clips


def save_dataset(df, output_path):
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        output_path,
        index=False
    )

    print(
        f"Saved cleaned dataset to: "
        f"{output_path}"
    )


def build_dataset(df):
    df = clean_columns(df)

    df = clean_numeric_columns(df)

    df = clean_text_columns(df)

    df = add_clip_files(df)

    return df