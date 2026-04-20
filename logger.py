import requests, os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def send(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT, "text": msg[:4000]})

def send_video(path, cap):
    with open(path,"rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo",
                      data={"chat_id": CHAT, "caption": cap},
                      files={"video": f})