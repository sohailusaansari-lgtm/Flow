import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": PEXELS_API_KEY
}

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
# SEARCH IMAGE FROM PEXELS
# ---------------------------
def search_image(query, per_page=3):
    url = "https://api.pexels.com/v1/search"

    try:
        res = requests.get(url, headers=HEADERS, params={
            "query": query,
            "per_page": per_page
        })

        data = res.json()

        photos = data.get("photos", [])

        if not photos:
            return None

        # pick first high-res image
        return photos[0]["src"]["large"]

    except Exception as e:
        print("❌ Image API error:", e)
        return None


# ---------------------------
# DOWNLOAD IMAGE
# ---------------------------
def download_image(url, filename):
    try:
        img_data = requests.get(url, timeout=10).content

        with open(filename, "wb") as f:
            f.write(img_data)

        return True
    except:
        return False


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def download_images_from_sentences(sentences):
    clean_images()

    print("🖼️ Fetching images...")

    count = 0

    for i, sentence in enumerate(sentences):

        if count >= 20:  # 🔥 limit (prevents crash)
            break

        # use key words (first few words)
        query = " ".join(sentence.split()[:4])

        img_url = search_image(query)

        if not img_url:
            print(f"⚠️ No image for: {query}")
            continue

        filename = os.path.join(SAVE_DIR, f"{count}.jpg")

        success = download_image(img_url, filename)

        if success:
            print(f"✅ Downloaded: {filename}")
            count += 1
        else:
            print(f"❌ Failed: {query}")

    # ---------------------------
    # FALLBACK (VERY IMPORTANT)
    # ---------------------------
    if count == 0:
        print("⚠️ No images downloaded, adding fallback")

        # create 1 black image
        from PIL import Image
        img = Image.new("RGB", (720, 1280), (0, 0, 0))
        img.save(os.path.join(SAVE_DIR, "0.jpg"))


# ---------------------------
# BACKWARD COMPATIBILITY
# ---------------------------
def fetch_images(sentences):
    """
    Fix for old imports
    """
    return download_images_from_sentences(sentences)
