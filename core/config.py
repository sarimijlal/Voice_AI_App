import os
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

if not OPEN_API_KEY:
    raise RuntimeError("API key is required")