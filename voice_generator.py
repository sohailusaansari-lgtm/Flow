from openai import OpenAI
from gtts import gTTS
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT_FILE = "voice.mp3"


# ---------------------------
# 🎭 CATEGORY DETECTION
# ---------------------------
def detect_category(topic):

    topic_lower = topic.lower()

    if any(x in topic_lower for x in ["जन्नत", "जहन्नम", "कुरान", "islam"]):
        return "islamic"

    elif any(x in topic_lower for x in ["ocean", "समुद्र", "deep sea"]):
        return "ocean"

    elif any(x in topic_lower for x in ["mughal", "history", "इतिहास", "बादशाह"]):
        return "history"

    return "general"


# ---------------------------
# 🎙️ STYLE PROMPTS
# ---------------------------
def get_style_prompt(category):

    if category == "islamic":
        return """
        आवाज़: गहरी, शांत, भावनात्मक और सम्मानपूर्ण।
        बोलने का अंदाज़: धीरे, स्पष्ट, दिल को छूने वाला।
        """

    elif category == "ocean":
        return """
        आवाज़: रहस्यमयी, धीमी और सस्पेंस से भरी।
        बोलने का अंदाज़: धीरे-धीरे, curiosity पैदा करने वाला।
        """

    elif category == "history":
        return """
        आवाज़: दमदार, शाही और प्रभावशाली।
        बोलने का अंदाज़: कहानी सुनाने जैसा, ताकत के साथ।
        """

    else:
        return """
        आवाज़: सामान्य, साफ और engaging।
        """


# ---------------------------
# 🎤 OPENAI TTS
# ---------------------------
def openai_tts(text, topic):

    try:
        category = detect_category(topic)
        style = get_style_prompt(category)

        styled_text = f"""
        {style}

        टेक्स्ट:
        {text}
        """

        print(f"🎭 Voice Style: {category}")

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=styled_text
        )

        with open(OUTPUT_FILE, "wb") as f:
            f.write(response.content)

        return OUTPUT_FILE

    except Exception as e:
        print("❌ OpenAI TTS failed:", e)
        return None


# ---------------------------
# 🟡 FALLBACK (ALWAYS WORKS)
# ---------------------------
def gtts_fallback(text):
    print("⚠️ Using gTTS fallback")

    tts = gTTS(text=text, lang="hi")
    tts.save(OUTPUT_FILE)

    return OUTPUT_FILE


# ---------------------------
# 🔍 VALIDATION
# ---------------------------
def is_valid(path):
    return path and os.path.exists(path) and os.path.getsize(path) > 5000


# ---------------------------
# 🎯 MAIN FUNCTION
# ---------------------------
def create_voice(text, topic):

    print("🎤 Generating dynamic voice...")

    audio = openai_tts(text, topic)

    if is_valid(audio):
        print("✅ Dynamic voice ready")
        return audio

    return gtts_fallback(text)
