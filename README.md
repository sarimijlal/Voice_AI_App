# 🎙️ Live Transcription & Translation Prototype

This project is a prototype web app that allows users to record speech, transcribe it, and translate the **complete transcript** into a target language. The translated text can also be played back using text-to-speech (TTS).  

---

##  Features
-  **Live Audio Recording** – Capture microphone input in real-time.  
-  **Chunked Transcription** – Audio is recorded in small chunks and combined later.  
-  **One-time Translation** – After stopping recording, the full transcript is translated into the target language.  
- **Text-to-Speech (TTS)** – Listen to the translated text as natural audio.  
- **Simple Web UI** – Start/stop recording, select languages, and playback translation.  

---

## Tech Stack
- **Frontend**: HTML, CSS, Vanilla JavaScript  
- **Backend**: FastAPI (Python)  
- **APIs**: OpenAI Whisper for transcription, OpenAI GPT for translation, OpenAI TTS for speech  
- **Deployment**: Render (backend), GitHub Pages or Render (frontend)  

---

##  Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/live-transcription-translation.git
cd live-transcription-translation 
```
### 2. Create a Virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```
### 3. Set environment variables
create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key_here

### 4. Run the backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Run the frontend
Open index.html in your browser
**Replace the URL of the endpoints fetch in <script> with your local URL**
