from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

from main import run

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ---------------------------
# /start
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Upload Video", callback_data="upload")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 AI Video Bot Ready\n\nClick below to upload:",
        reply_markup=reply_markup
    )


# ---------------------------
# BUTTON HANDLER
# ---------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "upload":
        await query.message.reply_text("⏳ Generating video...")

        result = run()

        if result:
            await query.message.reply_text(
                f"✅ Uploaded!\n\n🎬 {result['title']}\n🔗 {result['link']}"
            )
        else:
            await query.message.reply_text("❌ Failed. Check logs.")


# ---------------------------
# MAIN BOT
# ---------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
