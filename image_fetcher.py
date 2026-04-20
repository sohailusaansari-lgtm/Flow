import os, requests
from dotenv import load_dotenv

load_dotenv()

PEXELS = os.getenv("PEXELS_API_KEY")


def get_keywords(sentence):
    return " ".join(sentence.split()[:4])


def download_images_from_sentences(sentences):
    if not os.path.exists("images"):
        os.makedirs("images")

    headers = {"Authorization": PEXELS}

    for i, sentence in enumerate(sentences):
        query = get_keywords(sentence)

        url = "https://api.pexels.com/v1/search"
        params = {"query": query, "per_page": 1}

        r = requests.get(url, headers=headers, params=params).json()

        if r.get("photos"):
            img_url = r["photos"][0]["src"]["portrait"]
            img_data = requests.get(img_url).content

            with open(f"images/img_{i}.jpg", "wb") as f:
                f.write(img_data)