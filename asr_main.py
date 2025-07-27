# main.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
print("✅ FastAPI import successful")
import shutil
print("✅ Shutil import successful")
import uuid
print("✅ UUID import successful")
import os
print("✅ OS import successful")
from run_asr import audio_to_text 
print("✅ ASR import successful")

app = FastAPI()
print("✅ FastAPI app created")

os.makedirs("src", exist_ok=True)

@app.post("/asr/")
async def transcribe(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"./src/asrFiles/{file_id}.wav"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = audio_to_text(file_path)
        return {"text": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
