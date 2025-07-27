#!/bin/zsh
# Activate conda environment and run FastAPI server

# Change 'espnet-env' to your actual conda env name if different
conda activate espnet-env

# Install dependencies (optional, uncomment if needed)
# pip install fastapi uvicorn torch torchaudio soundfile espnet sounddevice numpy

# Start FastAPI server
uvicorn asr_main:app --reload --port 8001
