import random


def generate_thumbnails(title):
    return [
        {"style": "EMOTIONAL FACE 😱", "file": "thumb1.jpg"},
        {"style": "BIG TEXT + ARROW ➡️", "file": "thumb2.jpg"},
        {"style": "DARK MYSTERY 👀", "file": "thumb3.jpg"},
    ]


def predict_ctr(thumbnails, title):
    scores = {}

    for t in thumbnails:
        score = 0
        style = t["style"]

        # 🎯 CTR logic
        if "😱" in style:
            score += 30
        if "➡️" in style:
            score += 25
        if "👀" in style:
            score += 20

        # title influence
        if "secret" in title.lower():
            score += 20
        if "shocking" in title.lower():
            score += 25

        # randomness (trend factor)
        score += random.randint(10, 40)

        scores[t["file"]] = score

    best = max(scores, key=scores.get)

    return best, scores