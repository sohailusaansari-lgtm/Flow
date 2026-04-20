import requests, os
from dotenv import load_dotenv

load_dotenv()

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
        data={"chat_id": os.getenv("TELEGRAM_CHAT_ID"), "text": msg}
    )