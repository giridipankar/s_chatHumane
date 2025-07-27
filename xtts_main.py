# main.py
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
print("✅ FastAPI import successful")
import os
print("✅ OS import successful")
from run_xtts import text_to_speech_with_reasoning
print("✅ TTS import successful")

app = FastAPI()
print("✅ FastAPI app created")

os.makedirs("src", exist_ok=True)

@app.post("/tts/")
async def tts(text: str = Form(...)):
    try:
        # Check for explanation keywords
        explanation_keywords = ["explain", "describe", "elaborate"]
        explain = any(keyword in text.lower() for keyword in explanation_keywords)
        out_path = text_to_speech_with_reasoning(text, explain=explain)
        return FileResponse(out_path, media_type="audio/wav", filename="xtts_output.wav")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
