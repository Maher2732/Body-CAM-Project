# Body Camera Risk Analysis

This project processes annotated body-camera video data for safety-risk analysis.

## Current Features

- Reads annotation data from Excel
- Downloads source videos
- Extracts timestamped clips
- Skips duplicate clips
- Logs clip extraction errors

## Setup

See:

SETUP_INSTRUCTIONS.txt

## Project Structure

- `src/` - data preparation code
- `src/llm/` - LLM / multimodal model experiments
- `data/` - Excel data and local video folders
- `models/` - ML models
- `results/predictions/` - raw model outputs
- `results/metrics/` - scores vs. ground truth
- `config.example.json` - example local configuration