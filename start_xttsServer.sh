#!/bin/zsh
# Activate conda environment and run FastAPI server

# Change 'xtts-env' to your actual conda env name if different
conda activate xtts-env

# Install dependencies (optional, uncomment if needed)
# pip install fastapi uvicorn torch torchaudio soundfile espnet sounddevice numpy

# Start FastAPI server
uvicorn xtts_main:app --reload
