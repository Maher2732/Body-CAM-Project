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

- `src/` - Python source code
- `data/` - Excel data and local video folders
- `Models/` - ML models
- `results/` - experiment results
- `config.example.json` - example local configuration