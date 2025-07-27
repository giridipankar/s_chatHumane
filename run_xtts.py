from TTS.api import TTS
import os
import platform
import requests

print("Loading TTS model...")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    print("TTS model loaded successfully.")
except Exception as e:
    print(f"Error loading TTS model: {e}")

def text_to_speech(text, output_path="./src/ttsFiles/output.wav"):
    try:
        print("Generating speech...")
        tts.tts_to_file(text=text,
                        file_path=output_path,
                        speaker_wav="./src/audioFiles/sample-2.wav",
                    language="en")
        return output_path                                    
        print("Speech generated and saved!!")
    except Exception as e:
        print(f"Error during speech generation: {e}")

def deepseek_reasoning(text, ollama_url="http://localhost:11434/api/generate", model="deepseek-r1:7b", explain=False):
    # Add conversational prompt logic
    if not explain:
        prompt = f"Reply conversationally and keep it short. If asked to explain, provide details.\nUser: {text}"
    else:
        prompt = f"Explain in detail: {text}"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    print(f"Sending text to DeepSeek Ollama: {prompt}")
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        result = response.json()
        reasoning_text = result.get("response", "")
        # Extract only the final answer (last line or sentence)
        print(f"DeepSeek response: {reasoning_text}")
        if reasoning_text:
            # Try to get the last non-empty line
            lines = [line.strip() for line in reasoning_text.splitlines() if line.strip()]
            final_answer = lines[-1] if lines else reasoning_text
        else:
            final_answer = ""
        print(f"DeepSeek final answer: {final_answer}")
        return final_answer
    except Exception as e:
        print(f"Error querying DeepSeek Ollama: {e}")
        return ""

def text_to_speech_with_reasoning(text, output_path="./src/ttsFiles/output.wav", explain=False):
    # Intercept text, process with DeepSeek, then synthesize speech
    reasoning_text = deepseek_reasoning(text, explain=explain)
    return text_to_speech(reasoning_text, output_path)
