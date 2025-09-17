from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import io
import tempfile
from openai import OpenAI
from core.config import OPEN_API_KEY


app = FastAPI()

app.mount("/static", StaticFiles(directory=".", html=True), name= "static")

# Allow local dev + Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        # print("Received file:", audio.filename, "size:", len(contents), "bytes")
        audio_bytes = io.BytesIO(contents)
        audio_bytes.name = audio.filename

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


@app.post("/translate")
async def translate_text(text: str = Form(...), language: str = Form(None)):
    try:

        target_language = language.strip() if language and language.strip() else "English"


        prompt = f"""
            You are a professional translator. Your task is to translate the following conversation transcript into {target_language} without any commentary, just a plan translation string.

            Instructions:
            1. Preserve the exact meaning and nuance of the original text.
            2. The conversation could be between a patient and a doctor but it isn't neccessary.
            3. Be extremely careful with(if there are any) medical terms, drug names, procedures, and measurements.
            4. Avoid paraphrasing medical instructions; translate them accurately and clearly.
            5. Keep the formatting readable, preserving line breaks or speaker labels if present.

            Text to translate: {text}
            """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        translated = response.choices[0].message.content
        return JSONResponse({"translated": translated})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

@app.post("/speak")
async def speak_text(text: str = Form(...)):
    try:
        
        tts_response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
            #language=language
        )

        audio_bytes = tts_response.read()

        # Write audio bytes to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.write(audio_bytes)
        temp_file.seek(0)

        # Return as streaming response
        return StreamingResponse(temp_file, media_type="audio/mpeg", headers={
            "Content-Disposition": f"inline; filename=tts.mp3"
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)