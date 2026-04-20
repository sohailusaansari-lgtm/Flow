# ================================
# 🔥 GLOBAL FIX (VERY IMPORTANT)
# ================================
import PIL.Image

if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS


# ================================
# 📦 IMPORTS
# ================================
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ai_brain import generate_idea
from decision_engine import choose_topic
from image_fetcher import fetch_images
from image_processor import process_images
from video_creator import create_video
from analytics import save_metrics
from logger import log


# ================================
# 🔑 CONFIG
# ================================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ================================
# 🤖 TELEGRAM COMMANDS
# ================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is live!\nUse /generate to create video")


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⚙️ Generating video... Please wait")

        log("🚀 Generation started")

        # 🧠 AI pipeline
        idea = generate_idea()
        topic = choose_topic(idea)

        log(f"📌 Topic: {topic}")

        images = fetch_images(topic)
        processed_images = process_images(images)

        video_path = create_video(processed_images)

        save_metrics(topic, video_path)

        # ✅ Send result
        if video_path and os.path.exists(video_path):
            await update.message.reply_video(video=open(video_path, "rb"))
        else:
            await update.message.reply_text("❌ Failed to create video")

        log("✅ Generation complete")

    except Exception as e:
        log(f"❌ Error: {e}")
        await update.message.reply_text(f"Error: {e}")


# ================================
# 🚀 RUN BOT
# ================================
def main():
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set in environment")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    print("🤖 Bot running...")
    app.run_polling()


# ================================
# ▶️ ENTRY POINT
# ================================
if __name__ == "__main__":
    main()