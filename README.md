# Body Camera Risk Analysis

Can large language models (LLMs) and other multimodal models identify safety-risk
factors in police body-camera footage as accurately as human annotators?

This project holds the pipeline that prepares the data, and the experiments that
compare model predictions against a human-annotated ground-truth dataset.

## What it does

1. Reads the human annotations (`data/labdata_1.xlsx`): activity, weapon, fighting
   stance, sudden movement, facial expression, emotion, voice tone and an overall
   risk level (0-5), per person and time window.
2. Downloads the source videos and cuts a clip for each annotated time window.
3. Cleans the annotations and links every row to its clip
   (`data/cleaned_annotations.xlsx`).
4. Summarises the data (class balance, missing values, rows per video, risk by
   category, correlations) and reports a majority-class baseline for the risk groups.
5. LLM experiments (in progress): send clips to models such as Gemini and score their
   answers against the human labels (`src/llm/`).

## Setup and usage

See [SETUP_INSTRUCTIONS.txt](SETUP_INSTRUCTIONS.txt). Short version:

```bash
python src/main.py                    # full pipeline
python src/main.py --skip-download    # reuse the videos already downloaded
```

## Project structure

- `src/` - data preparation and analysis code
- `src/llm/` - LLM / multimodal model experiments
- `data/` - annotations (tracked); `videos/` and `clips/` are local only
- `models/` - trained models
- `results/predictions/` - raw model outputs
- `results/metrics/` - scores vs. ground truth
- `config.example.json` - copy to `config.json` and fill in local paths
- `.env.example` - copy to `.env` and add your API key (never commit `.env`)

## Data note

The annotations describe real people in publicly posted police footage, including
perceived race and gender, injuries and deaths. Handle and share them accordingly.
