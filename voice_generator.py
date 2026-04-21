import os
import requests
from dotenv import load_dotenv

# fallback imports
from gtts import gTTS

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # FREE usable

OUTPUT_FILE = "voice.mp3"


# ---------------------------
# 🎙️ ELEVENLABS (REALISTIC)
# ---------------------------
def elevenlabs_tts(text):

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.6,
            "use_speaker_boost": True
        }
    }

    try:
        res = requests.post(url, json=data, headers=headers, timeout=30)

        if res.status_code != 200:
            print("❌ ElevenLabs failed:", res.text)
            return None

        with open(OUTPUT_FILE, "wb") as f:
            f.write(res.content)

        return OUTPUT_FILE

    except Exception as e:
        print("❌ ElevenLabs exception:", e)
        return None


# ---------------------------
# 🎤 COQUI (OFFLINE REAL VOICE)
# ---------------------------
def coqui_tts(text):
    try:
        from TTS.api import TTS

        print("🔁 Using Coqui TTS (realistic Hindi)")

        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

        tts.tts_to_file(
            text=text,
            file_path=OUTPUT_FILE,
            speaker_wav=None,
            language="hi"
        )

        return OUTPUT_FILE

    except Exception as e:
        print("❌ Coqui failed:", e)
        return None


# ---------------------------
# 🟡 gTTS (LAST FALLBACK)
# ---------------------------
def gtts_fallback(text):
    print("⚠️ Using gTTS fallback")

    tts = gTTS(text=text, lang="hi")
    tts.save(OUTPUT_FILE)

    return OUTPUT_FILE


# ---------------------------
# 🔍 VALIDATION
# ---------------------------
def is_valid_audio(path):
    return path and os.path.exists(path) and os.path.getsize(path) > 5000


# ---------------------------
# 🎯 MAIN FUNCTION
# ---------------------------
def create_voice(text):

    print("🎤 Generating voice...")

    # 1️⃣ ElevenLabs
    audio = elevenlabs_tts(text)
    if is_valid_audio(audio):
        print("✅ ElevenLabs voice ready")
        return audio

    # 2️⃣ Coqui (realistic offline)
    audio = coqui_tts(text)
    if is_valid_audio(audio):
        print("✅ Coqui voice ready")
        return audio

    # 3️⃣ gTTS (guaranteed)
    audio = gtts_fallback(text)
    print("✅ gTTS voice ready")
    return audio
