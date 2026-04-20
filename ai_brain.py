import os
import random
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

USED_FILE = "used_topics.txt"

# ---------------------------
# 🎯 CATEGORIES
# ---------------------------
CATEGORIES = [
    "History facts",
    "Ocean mysteries",
    "Mughal Empire",
    "Quranic stories",
    "Jannat and Jahannam"
]


# ---------------------------
# 🧠 AI CALL
# ---------------------------
def ask_ai(prompt):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()


# ---------------------------
# 🔁 UNIQUE TOPIC
# ---------------------------
def is_used(topic):
    if not os.path.exists(USED_FILE):
        return False
    with open(USED_FILE, "r") as f:
        return topic in f.read()


def save_topic(topic):
    with open(USED_FILE, "a") as f:
        f.write(topic + "\n")


def get_topic():
    category = random.choice(CATEGORIES)

    # 🔥 Special handling for Islamic topics
    if category in ["Quranic stories", "Jannat and Jahannam"]:
        prompt = f"""
        Generate ONE meaningful Hindi topic about: {category}

        Rules:
        - Must be based on authentic Islamic concepts
        - No fake or exaggerated claims
        - Emotional and reflective
        - Short (1 line)
        - Curiosity driven but respectful

        Example:
        "जन्नत की वो नेमत जो इंसान सोच भी नहीं सकता"
        "जहन्नम की सजा जो दिल हिला दे"
        """
    else:
        prompt = f"""
        Generate ONE viral Hindi topic about: {category}

        Rules:
        - Shocking / mysterious
        - Very specific
        - Not commonly known
        - Curiosity-driven
        - One line only
        """

    return ask_ai(prompt).strip()


def get_unique_topic():
    for _ in range(5):
        t = get_topic()
        if not is_used(t):
            save_topic(t)
            return t
    return get_topic()


# ---------------------------
# ✂️ SENTENCES
# ---------------------------
def split_sentences(script):
    sentences = re.split(r'[।.!?]', script)
    return [s.strip() for s in sentences if s.strip()]


# ---------------------------
# 🎬 CONTENT GENERATION
# ---------------------------
def generate_content():
    topic = get_unique_topic()

    # 🔥 Islamic content handling
    if any(word in topic.lower() for word in ["जन्नत", "जहन्नम", "कुरान"]):
        prompt = f"""
        Topic: {topic}

        Write a 40-55 second Hindi story.

        Rules:
        - Respectful tone
        - Based on Islamic teachings
        - No exaggeration or fake info
        - Emotional and powerful
        - Simple Hindi
        - No "subscribe", no "video"

        Start directly like storytelling.
        End with a meaningful reflection.
        """
    else:
        prompt = f"""
        Topic: {topic}

        Write a 40-55 second Hindi story.

        Rules:
        - Hook in first line
        - Suspense + curiosity
        - Short sentences
        - No "Did you know"
        - No "इस वीडियो में"
        - End with twist

        Output only story.
        """

    script = ask_ai(prompt)
    sentences = split_sentences(script)

    return {
        "topic": topic,
        "script": script,
        "sentences": sentences
    }


# ---------------------------
# 🏷️ METADATA
# ---------------------------
def generate_metadata(script, topic):

    title = ask_ai(f"""
    Create a SHORT Hindi viral title (max 6 words)

    Topic: {topic}

    Rules:
    - Very catchy
    - Curiosity driven
    - Include #shorts
    """)

    if not title:
        title = "😱 Viral Fact #shorts"

    if "#shorts" not in title:
        title += " #shorts"

    tags = "#shorts #viral #history #islamic #facts #ocean"

    return title.strip(), tags


# ---------------------------
# BACKWARD FIX
# ---------------------------
def generate_idea():
    return generate_content()
