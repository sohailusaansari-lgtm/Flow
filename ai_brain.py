import os
import re
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

USED_FILE = "used_topics.txt"

# ---------------------------
# AI CALL
# ---------------------------
def ask_ai(prompt):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()


# ---------------------------
# CATEGORY CONTROL
# ---------------------------
CATEGORIES = [
    "History facts",
    "Ocean mysteries",
    "Mughal Empire"
]


def get_topic():
    category = random.choice(CATEGORIES)

    prompt = f"""
    Generate ONE viral Hindi topic about: {category}

    Rules:
    - Shocking / mysterious
    - Very specific (not generic)
    - Not commonly known
    - Curiosity-driven
    - One line only

    Examples:
    "समुद्र का वो हिस्सा जहां कुछ भी नहीं रहता"
    "औरंगज़ेब का सबसे खतरनाक फैसला"
    "इतिहास का सबसे छोटा युद्ध"
    """

    return ask_ai(prompt).strip()


# ---------------------------
# UNIQUE TOPIC SYSTEM
# ---------------------------
def is_used(topic):
    if not os.path.exists(USED_FILE):
        return False
    with open(USED_FILE, "r") as f:
        return topic in f.read()


def save_topic(topic):
    with open(USED_FILE, "a") as f:
        f.write(topic + "\n")


def get_unique_topic():
    for _ in range(5):
        t = get_topic()
        if not is_used(t):
            save_topic(t)
            return t
    return get_topic()


# ---------------------------
# SENTENCE SPLIT
# ---------------------------
def split_sentences(script):
    sentences = re.split(r'[।.!?]', script)
    return [s.strip() for s in sentences if s.strip()]


# ---------------------------
# CONTENT GENERATION
# ---------------------------
def generate_content():
    topic = get_unique_topic()

    script = ask_ai(f"""
    Topic: {topic}

    Write a 40-55 second Hindi story.

    STRICT RULES:
    - DO NOT say "Did you know"
    - DO NOT say "इस वीडियो में"
    - DO NOT mention "video", "channel", "subscribe"
    - Start directly with story (like movie scene)
    - Add suspense + curiosity
    - Keep sentences short
    - End with twist or shocking reveal

    Output only story text.
    """)

    sentences = split_sentences(script)

    return {
        "topic": topic,
        "script": script,
        "sentences": sentences
    }


# ---------------------------
# TITLE + TAGS
# ---------------------------
def generate_metadata(script, topic):
    title = ask_ai(f"""
    Create a SHORT Hindi clickbait title (max 6 words).

    Topic: {topic}

    Rules:
    - Must NOT be empty
    - Must be highly clickable
    - Add curiosity
    - Include #shorts
    """)

    # safety fallback
    if not title or len(title.strip()) == 0:
        title = "😱 Viral Fact #shorts"

    title = title.strip()

    if "#shorts" not in title:
        title += " #shorts"

    if len(title) > 100:
        title = title[:100]

    tags = "#shorts #viral #history #facts #india"

    return title, tags