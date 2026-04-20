import os
import asyncio
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# 🔥 ONLY import from main
from main import run, start_auto

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# prevent multiple runs
is_running = False


# ---------------------------
# /start COMMAND
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Upload Video", callback_data="upload")]
    ]

    await update.message.reply_text(
        "🤖 AI Video Bot Ready\n\nClick below to upload:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------------------
# BUTTON HANDLER
# ---------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running

    query = update.callback_query
    await query.answer()

    if query.data == "upload":

        if is_running:
            await query.edit_message_text("⚠️ Already running, please wait...")
            return

        is_running = True

        await query.edit_message_text("🚀 Starting video generation...")

        loop = asyncio.get_running_loop()

        def task():
            global is_running
            try:
                run()  # 🔥 YOUR MAIN PIPELINE
            except Exception as e:
                print("❌ Error:", e)
            finally:
                is_running = False

        # run without blocking bot
        loop.run_in_executor(None, task)

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⏳ Processing started... updates will follow."
        )


# ---------------------------
# MAIN BOT
# ---------------------------
def main():
    if not TOKEN:
        raise Exception("❌ TELEGRAM_BOT_TOKEN missing in .env")

    # 🔥 Start 5-hour auto loop
    start_auto()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot running...")
    app.run_polling()


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    main()
