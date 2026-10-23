import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from config import config
from data_read import read_data
from dataset_builder import COLUMN_RENAMES

# The factors the LLM is asked about (cleaned column names)
ANNOTATION_COLUMNS = [
    "activity",
    "weapon",
    "fighting stance",
    "sudden movement",
    "gesture",
    "conflict escalation gesture",
    "conflict_escalation_gesture",
    "conflict_escalation_gesture_impact",
    "face visible",
    "facial expression",
    "emotion",
    "conflict escation facial",
    "facial expression type",
    "facial expression impact",
    "facial escalation cause impact",
    "impact resulting from facial escalation",
    "facial aggression",
    "stress",
    "lying",
    "ifspeaking",
    "voice tone",
    "conflict escalation voice",
    "escalation causing voice and speech patterns",
    "impact resulting from voice and speech patterns",
    "escalation sentence",
    "hostility level speech",
    "distress level",
    "location",
    "type of instance",
    "officer experience",
    "gender",
    "race",
    "call for backup",
    "risk level",
    "audit or normal",
    "person injured",
    "dead or unconscious",
    "has the person died",
]

# Columns the model can't answer: "person" is an ID (p1, s1, ...) it has no way to know
NOT_ANSWERABLE = {"person"}

# Above this many distinct answers, let the model answer in short free text
MAX_CHOICES = 25

OPENING = (
    "You are labelling a police body-camera video clip.\n"
    "The labels describe the SUSPECT: the person the officers are dealing with. "
    "If several people qualify, use the most prominent one.\n"
    "Use both what you see and what you hear. Answer only from what is in the clip.\n"
    'If a factor cannot be determined from the clip, answer "unknown".\n'
)

CLOSING = (
    "Return ONLY a JSON object with exactly one key per factor above, "
    "using the factor name as the key. No other text."
)


def load_instructions():
    """The annotators' question for each column (row 0 of the raw spreadsheet)."""
    raw_row = read_data(config["excel_path"]).iloc[0]

    return {
        COLUMN_RENAMES.get(raw_name, raw_name): str(text)
        for raw_name, text in raw_row.items()
    }


def split_answers(values):
    """Single answers like 'falling; laying down' become separate choices."""
    return sorted({part.strip() for value in values for part in value.split(";")})


def describe_options(column):
    values = column.dropna()

    if pd.api.types.is_numeric_dtype(values):
        low, high = int(values.min()), int(values.max())

        # Annotators typed -1 for "not applicable" (face not visible, not speaking)
        if low == -1:
            return f"an integer from 0 to {high}, or -1 if not applicable"

        return f"an integer from {low} to {high}"

    choices = split_answers(values)

    if len(choices) > MAX_CHOICES:
        return "short free text"

    # Only offer "several" when annotators actually combined answers with ';'
    if values.str.contains(";").any():
        return "one or more of: " + ", ".join(choices) + " (separate several with '; ')"

    return "one of: " + ", ".join(choices)


def usable_columns(columns, df):
    """Drop columns the model can't answer or that never vary (nothing to score)."""
    return [
        name
        for name in columns
        if name not in NOT_ANSWERABLE and df[name].dropna().nunique() > 1
    ]


def build_prompt(columns, df=None):
    if df is None:
        df = read_data(config["cleaned_dataset"])

    instructions = load_instructions()

    factors = [
        f"- {name}: {instructions[name]}\n  Answer: {describe_options(df[name])}"
        for name in usable_columns(columns, df)
    ]

    return OPENING + "\nFactors:\n" + "\n".join(factors) + "\n\n" + CLOSING


if __name__ == "__main__":
    cleaned = read_data(config["cleaned_dataset"])
    used = usable_columns(ANNOTATION_COLUMNS, cleaned)
    skipped = [name for name in ANNOTATION_COLUMNS if name not in used]

    print(build_prompt(ANNOTATION_COLUMNS, cleaned))
    print(f"\n--- {len(used)} factors used; skipped: {skipped}")
