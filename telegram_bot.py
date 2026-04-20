from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ai_brain import generate_idea
from decision_engine import choose_topic
from image_fetcher import fetch_images
from image_processor import process_images
from video_creator import create_video


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is ready!")


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Generating video...")

    idea = generate_idea()
    topic = choose_topic(idea)
    images = fetch_images(topic)
    processed = process_images(images)
    video = create_video(processed)

    await update.message.reply_text(f"✅ Done!\n{video}")


def run_bot(token):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    app.run_polling()