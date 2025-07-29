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
                        speaker_wav="./src/audioFiles/eldora.wav",
                    language="en")
        return output_path                                    
        print("Speech generated and saved!!")
    except Exception as e:
        print(f"Error during speech generation: {e}")

def deepseek_reasoning(text, ollama_url="http://localhost:11434/api/generate", model="deepseek-r1:7b", explain=False):
    # Add conversational prompt logic
    if not explain:
        prompt = f"Keep it precise & chatty:\nUser: {text}:"
    else:
        prompt = f"Explain in detail:\nUser: {text}"
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
            # Remove any <think> block and return only the final answer
            if '<think>' in reasoning_text:
                import re
                final_answer = re.sub(r'<think>.*?</think>', '', reasoning_text, flags=re.DOTALL).strip()
            else:
                final_answer = reasoning_text
            # Remove emojis from the final answer
            final_answer = re.sub(r'[\U00010000-\U0010ffff\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', '', final_answer)
            final_answer = final_answer.encode('ascii', 'ignore').decode('ascii')
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
