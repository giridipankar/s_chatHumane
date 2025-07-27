# s_chatHumane

## Usage

### 1. Enable your Python environment (macOS/zsh)

If using conda:

```sh
source start_xttsServer.sh
```

```sh
source start_espnetServer.sh
```

## or

```sh
conda activate espnet-env
```

If using venv:

```sh
source path/to/venv/bin/activate
```

### 2. Install dependencies

```sh
pip install fastapi uvicorn torch torchaudio soundfile espnet sounddevice numpy
```

### 3. Start the FastAPI server

```sh
uvicorn main:app --reload
```

### 4. Endpoints

- **POST /asr/**  
  Upload a WAV file to get its transcription.

- **POST /tts/**  
  Send text to receive a synthesized WAV file.

---

## Overview

This project provides a FastAPI-based web service for speech-to-text (ASR) and text-to-speech (TTS) using ESPnet models.

---

## Dependencies

Install the following Python packages:

```sh
pip install fastapi uvicorn torch torchaudio soundfile espnet
```

If you use TTS playback, also install:

```sh
pip install sounddevice numpy
```

---

## Directory Structure

```
s_chatHumane/
├── main.py
├── run_asr.py
├── run_tts.py
├── README.md
└── src/
    ├── audioFiles/
    └── ttsFiles/
```

---

## Notes

- The ASR and TTS models are loaded from Hugging Face by default. Internet access is required for first-time use.
- If you want to use local models, download and unpack the ESPnet model into a directory and update the path in `run_asr.py` and `run_tts.py`.

---

## Example Request (ASR)

```sh
curl -X POST "http://127.0.0.1:8001/asr/" -F "file=@your_audio.wav"
```

## Example Request (TTS)

```sh
curl -X POST "http://127.0.0.1:8000/tts/" -F "text=Hello world"
```

---

## Troubleshooting

- If you see errors about missing modules, ensure all dependencies are installed in your Python environment.
- For model loading errors, check your internet connection or verify local model paths and structure.
