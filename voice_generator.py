import os
import requests
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "kug5BkLLkmHNdMkhpz3d"


def enhance(script):
    return script.replace("।", "... ")


def create_voice(script):
    script = enhance(script)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API,
        "Content-Type": "application/json"
    }

    data = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.85
        }
    }

    print("🎤 Using ElevenLabs Voice ID:", VOICE_ID)

    r = requests.post(url, json=data, headers=headers)

    print("📡 ElevenLabs status:", r.status_code)

    if r.status_code != 200:
        print("❌ ElevenLabs ERROR:", r.text)
        raise Exception("ElevenLabs failed — fix API/voice")

    with open("voice.mp3", "wb") as f:
        f.write(r.content)

    print("✅ ElevenLabs voice USED")

    return "voice.mp3"