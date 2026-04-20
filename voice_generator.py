import os
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # FREE voice
OUTPUT_FILE = "voice.mp3"


def create_voice(text):

    if not ELEVEN_API_KEY:
        print("❌ Missing API key → fallback")
        return create_fallback_audio(text)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    try:
        res = requests.post(url, json=data, headers=headers, timeout=30)

        print("🔊 ElevenLabs:", res.status_code)

        if res.status_code != 200:
            print(res.text)
            return create_fallback_audio(text)

        with open(OUTPUT_FILE, "wb") as f:
            f.write(res.content)

        # validate
        if os.path.getsize(OUTPUT_FILE) < 1000:
            return create_fallback_audio(text)

        return OUTPUT_FILE

    except Exception as e:
        print("❌ Voice error:", e)
        return create_fallback_audio(text)


# 🔥 FIXED FALLBACK (DYNAMIC LENGTH)
def create_fallback_audio(text):
    print("⚠️ Using fallback audio")

    words = len(text.split())
    duration = max(40, min(55, words / 2.5))  # 🔥 key fix

    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=mono",
        "-t", str(duration),
        "-q:a", "9",
        "-acodec", "libmp3lame",
        OUTPUT_FILE
    ])

    return OUTPUT_FILE
