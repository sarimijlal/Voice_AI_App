from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, Form
import tempfile
import io
import os
from openai import OpenAI
from core.config import OPEN_API_KEY
# Initialize FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory=".", html=True), name= "static")

# Allow local dev + Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client (new style)
client = OpenAI(api_key=OPEN_API_KEY)

@app.post("/transcribe-chunk")
async def transcribe_chunk(
    audio: UploadFile,
    language: str = Form(None),
    prompt: str = Form(None)
):
    try:
        
        # Read file fully into memory
        contents = await audio.read()
        print("Received file:", audio.filename, "size:", len(contents), "bytes")
        audio_bytes = io.BytesIO(contents)
        audio_bytes.name = audio.filename  # preserve extension (important!)

        # Prepare kwargs
        kwargs = {"model": "whisper-1", "file": audio_bytes}
        if language and language.strip():
            kwargs["language"] = language.strip()
        if prompt and prompt.strip():
            kwargs["prompt"] = prompt.strip()

        # Open temp file for reading
        transcription = client.audio.transcriptions.create(**kwargs)

        return JSONResponse({
            "text": transcription.text,
            "model": "whisper-1"
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

