import time
import traceback
import threading

from ai_brain import generate_content, generate_metadata
from image_fetcher import download_images_from_sentences
from voice_generator import create_voice
from video_generator import create_video
from thumbnail_generator import create_thumbnail
from youtube_uploader import upload_video
from logger import send, send_video

# ---------------------------
# GLOBAL LOCK (PREVENT DOUBLE RUN)
# ---------------------------
is_running = False


# ---------------------------
# MAIN PIPELINE
# ---------------------------
def run():
    global is_running

    if is_running:
        send("⚠️ Already running, skipping...")
        return

    is_running = True

    try:
        send("🚀 Starting new video...")

        # ---------------------------
        # 🧠 AI CONTENT
        # ---------------------------
        data = generate_content()
        send(f"🧠 Topic:\n{data['topic']}")

        # ---------------------------
        # 🖼️ IMAGES
        # ---------------------------
        send("🖼️ Fetching images...")
        download_images_from_sentences(data["sentences"])
        send("✅ Images ready")

        # ---------------------------
        # 🎤 VOICE
        # ---------------------------
        send("🎤 Generating voice...")
        audio = create_voice(data["script"])
        send("✅ Voice ready")

        # ---------------------------
        # 🎬 VIDEO
        # ---------------------------
        send("🎬 Creating video...")
        create_video("images", audio, data["sentences"])
        send("✅ Video ready")

        # ---------------------------
        # 🏷️ METADATA
        # ---------------------------
        title, tags = generate_metadata(data["script"], data["topic"])
        send(f"🏷️ Title:\n{title}")

        # ---------------------------
        # 🖼️ THUMBNAIL
        # ---------------------------
        send("🖼️ Creating thumbnail...")
        thumb = create_thumbnail(title)
        send("✅ Thumbnail ready")

        # ---------------------------
        # 📤 UPLOAD
        # ---------------------------
        send("📤 Uploading to YouTube...")
        link = upload_video(title, tags, thumb)

        send(f"✅ Uploaded successfully:\n{link}")

        # ---------------------------
        # 📹 SEND VIDEO TO TELEGRAM
        # ---------------------------
        send_video("output.mp4", title)

    except Exception as e:
        send(f"❌ ERROR:\n{str(e)}")
        send(traceback.format_exc())

    finally:
        is_running = False


# ---------------------------
# 🔁 AUTO LOOP (5 HOURS)
# ---------------------------
def auto_loop():
    while True:
        run()
        send("⏳ Waiting 5 hours...")
        time.sleep(18000)  # 5 hours


# ---------------------------
# START AUTO LOOP (BACKGROUND)
# ---------------------------
def start_auto():
    t = threading.Thread(target=auto_loop, daemon=True)
    t.start()


# ---------------------------
# OPTIONAL DIRECT RUN
# ---------------------------
if __name__ == "__main__":
    start_auto()
    while True:
        time.sleep(1)
