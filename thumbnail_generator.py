from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import textwrap

# 🎯 High-CTR Hindi power words
POWER_WORDS = [
    "चौंकाने वाला", "खतरनाक", "सच!", "हैरान",
    "राज", "मत देखो", "इतिहास", "डरावना"
]

# 🎨 Bright background colors (high contrast)
BG_COLORS = [
    (255, 50, 50),    # red
    (50, 150, 255),   # blue
    (255, 200, 0),    # yellow
    (120, 0, 255),    # purple
    (0, 200, 150)     # teal
]


def create_thumbnail(title):
    # ----------------------------
    # 🖼️ Create base background
    # ----------------------------
    width, height = 720, 1280
    bg_color = random.choice(BG_COLORS)
    bg = Image.new("RGB", (width, height), bg_color)

    draw = ImageDraw.Draw(bg)

    # ----------------------------
    # 🔤 Load font
    # ----------------------------
    try:
        font_big = ImageFont.truetype("arial.ttf", 110)
    except:
        font_big = ImageFont.load_default()

    # ----------------------------
    # 🧠 Shorten title (IMPORTANT)
    # ----------------------------
    words = title.split()
    short_title = " ".join(words[:3])  # keep 2–3 words max

    # ----------------------------
    # 💥 Add power word (random)
    # ----------------------------
    if random.random() > 0.5:
        short_title = random.choice(POWER_WORDS) + "\n" + short_title

    # ----------------------------
    # 📏 Wrap text nicely
    # ----------------------------
    wrapped_text = textwrap.fill(short_title, width=8)

    # ----------------------------
    # 🎯 Text position
    # ----------------------------
    x = 60
    y = height // 3

    # ----------------------------
    # 🌑 Shadow effect
    # ----------------------------
    draw.text((x + 6, y + 6), wrapped_text, font=font_big, fill="black")

    # ----------------------------
    # ✨ Main text
    # ----------------------------
    draw.text((x, y), wrapped_text, font=font_big, fill="white")

    # ----------------------------
    # 🔺 Highlight box (attention)
    # ----------------------------
    box_margin = 40
    draw.rectangle(
        (box_margin, y - 40, width - box_margin, y + 400),
        outline="yellow",
        width=10
    )

    # ----------------------------
    # 🌫️ Slight blur blend (cinematic)
    # ----------------------------
    blurred = bg.filter(ImageFilter.GaussianBlur(2))
    final_img = Image.blend(bg, blurred, 0.2)

    # ----------------------------
    # 💾 Save thumbnail
    # ----------------------------
    output_path = "thumbnail.jpg"
    final_img.save(output_path)

    return output_path