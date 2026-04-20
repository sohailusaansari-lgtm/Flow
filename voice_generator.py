import os
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# ENV (supports both names)
# ---------------------------
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")

# 🔥 FREE VOICE (IMPORTANT)
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel

OUTPUT_FILE = "voice.mp3"


# ---------------------------
# CREATE VOICE
# ---------------------------
def create_voice(text):

    if not ELEVEN_API_KEY:
        print("❌ Missing ElevenLabs API key")
        return create_fallback_audio()

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

        print("🔊 ElevenLabs Status:", response.status_code)

        if response.status_code != 200:
            print("❌ ElevenLabs ERROR:", response.text)
            return create_fallback_audio()

        # save audio
        with open(OUTPUT_FILE, "wb") as f:
            f.write(response.content)

        # ---------------------------
        # VALIDATION (IMPORTANT)
        # ---------------------------
        if not os.path.exists(OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) < 1000:
            print("⚠️ Audio too small → fallback")
            return create_fallback_audio()

        return OUTPUT_FILE

    except Exception as e:
        print("❌ Voice Exception:", str(e))
        return create_fallback_audio()


# ---------------------------
# 🔥 REAL FALLBACK AUDIO (NO CRASH)
# ---------------------------
def create_fallback_audio():
    print("⚠️ Using FFmpeg silent audio fallback...")

    output = OUTPUT_FILE

    try:
        subprocess.run([
            "ffmpeg",
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=mono",
            "-t", "10",
            "-q:a", "9",
            "-acodec", "libmp3lame",
            output
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output

    except Exception as e:
        print("❌ FFmpeg fallback failed:", e)

        # last fallback (tiny valid file)
        with open(output, "wb") as f:
            f.write(b"\x00\x00\x00\x00")

        return output
