import json, os

FILE = "performance.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    return json.load(open(FILE))

def save_data(data):
    json.dump(data, open(FILE, "w"), indent=2)

def log_video(topic, title, score):
    data = load_data()
    data.append({"topic": topic, "title": title, "score": score})
    save_data(data)

def estimate_score(script, title):
    s = script.lower()
    score = 0
    if "आप" in script: score += 2
    if "?" in script: score += 3
    if "सच" in script: score += 2
    return score

def get_best_patterns():
    data = load_data()
    if not data: return None
    top = sorted(data, key=lambda x: x["score"], reverse=True)[:5]
    return {
        "hooks": list(set([d["title"].split()[0] for d in top])),
        "topics": [d["topic"] for d in top]
    }