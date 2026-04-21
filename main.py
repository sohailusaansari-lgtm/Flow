import time
import traceback

from ai_brain import generate_idea, generate_metadata
from voice_generator import create_voice
from image_fetcher import download_images_from_sentences
from video_generator import create_video
from youtube_uploader import upload_video


# ---------------------------
# 🔥 MAIN WORKFLOW
# ---------------------------
def run():

    try:
        print("\n🚀 Starting AI Video Pipeline...\n")

        # ---------------------------
        # 🧠 AI BRAIN
        # ---------------------------
        data = generate_idea()

        topic = data["topic"]
        script = data["script"]
        sentences = data["sentences"]

        print(f"🧠 Topic: {topic}")
        print(f"📜 Script:\n{script}\n")

        # ---------------------------
        # 🎤 VOICE
        # ---------------------------
        audio = create_voice(script, topic)
        print("🎤 Voice ready:", audio)

        # ---------------------------
        # 🖼️ IMAGES (SMART)
        # ---------------------------
        download_images_from_sentences(sentences, topic)

        print("🖼️ Images generated")

        # ---------------------------
        # 🎬 VIDEO
        # ---------------------------
        create_video("images", audio, sentences)

        print("🎬 Video created")

        # ---------------------------
        # 🏷️ METADATA
        # ---------------------------
        title, tags = generate_metadata(script, topic)

        print("📝 Title:", title)
        print("🏷️ Tags:", tags)

        # ---------------------------
        # 📤 UPLOAD
        # ---------------------------
        link = upload_video(title, tags)

        print("✅ Uploaded:", link)

        return {
            "topic": topic,
            "title": title,
            "link": link
        }

    except Exception as e:
        print("❌ ERROR:\n", str(e))
        traceback.print_exc()
        return None


# ---------------------------
# 🔁 AUTO LOOP (5 HOURS)
# ---------------------------
def start_auto():

    print("⏳ Auto mode started (every 5 hours)\n")

    while True:

        result = run()

        if result:
            print(f"🎯 Done: {result['title']}")

        print("\n😴 Sleeping for 5 hours...\n")

        # 🔥 5 hours = 18000 seconds
        time.sleep(60 * 60 * 5)


# ---------------------------
# ▶️ ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    start_auto()
