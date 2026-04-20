import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# 🔥 USE FREE VOICE (IMPORTANT)
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel (FREE)

OUTPUT_FILE = "voice.mp3"


# ---------------------------
# CREATE VOICE
# ---------------------------
def create_voice(text):

    if not ELEVEN_API_KEY:
        raise Exception("❌ Missing ELEVEN_API_KEY in .env")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)

        # 🔍 DEBUG LOG
        print("🔊 ElevenLabs:", response.status_code)

        if response.status_code != 200:
            print("❌ ElevenLabs ERROR:", response.text)
            raise Exception("ElevenLabs failed — fix API/voice")

        with open(OUTPUT_FILE, "wb") as f:
            f.write(response.content)

        return OUTPUT_FILE

    except Exception as e:
        print("❌ Voice Exception:", str(e))

        # ---------------------------
        # 🔥 FALLBACK (NO CRASH)
        # ---------------------------
        return create_fallback_audio()


# ---------------------------
# FALLBACK AUDIO (IMPORTANT)
# ---------------------------
def create_fallback_audio():
    print("⚠️ Using fallback silent audio...")

    try:
        from moviepy.editor import AudioClip
        import numpy as np

        duration = 8  # seconds

        def silence(t):
            return [0]

        audio = AudioClip(silence, duration=duration)
        audio.write_audiofile(OUTPUT_FILE, fps=44100)

        return OUTPUT_FILE

    except Exception as e:
        print("❌ Fallback audio failed:", e)

        # last fallback (empty file)
        with open(OUTPUT_FILE, "wb") as f:
            f.write(b"")

        return OUTPUT_FILE
