import os
import requests
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

HEADERS = {"Authorization": PEXELS_API_KEY}
SAVE_DIR = "images"


# ---------------------------
# CLEAN OLD IMAGES
# ---------------------------
def clean_images():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        return

    for f in os.listdir(SAVE_DIR):
        try:
            os.remove(os.path.join(SAVE_DIR, f))
        except:
            pass


# ---------------------------
# 🧠 GENERATE VISUAL PROMPT
# ---------------------------
def generate_visual_prompt(sentence, topic):

    prompt = f"""
    Convert this into a cinematic visual search query:

    Topic: {topic}
    Sentence: {sentence}

    Rules:
    - Describe what should be SEEN visually
    - Use 2–5 words only
    - Be specific and vivid
    - No abstract words

    Example:
    "deep ocean glowing creatures"
    "mughal palace golden throne"
    "dark fire hell flames"
    """

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content.strip()


# ---------------------------
# SEARCH IMAGE
# ---------------------------
def search_image(query):
    url = "https://api.pexels.com/v1/search"

    try:
        res = requests.get(url, headers=HEADERS, params={
            "query": query,
            "per_page": 5
        })

        data = res.json()
        photos = data.get("photos", [])

        if not photos:
            return None

        # 🔥 pick random image (avoid repetition)
        choice = random.choice(photos)

        return choice["src"]["large"]

    except Exception as e:
        print("❌ Image API error:", e)
        return None


# ---------------------------
# DOWNLOAD IMAGE
# ---------------------------
def download_image(url, filename):
    try:
        img = requests.get(url, timeout=10).content
        with open(filename, "wb") as f:
            f.write(img)
        return True
    except:
        return False


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def download_images_from_sentences(sentences, topic):

    clean_images()

    print("🖼️ Generating smart visuals...")

    count = 0

    for i, sentence in enumerate(sentences):

        if count >= 15:
            break

        # 🧠 AI generates better query
        query = generate_visual_prompt(sentence, topic)

        print(f"🔍 {query}")

        img_url = search_image(query)

        if not img_url:
            continue

        filename = os.path.join(SAVE_DIR, f"{count}.jpg")

        if download_image(img_url, filename):
            print(f"✅ {filename}")
            count += 1

    # ---------------------------
    # FALLBACK
    # ---------------------------
    if count == 0:
        from PIL import Image
        img = Image.new("RGB", (720, 1280), (0, 0, 0))
        img.save(os.path.join(SAVE_DIR, "0.jpg"))


# ---------------------------
# BACKWARD COMPAT
# ---------------------------
def fetch_images(sentences):
    return download_images_from_sentences(sentences, "general")
