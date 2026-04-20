import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_video_titles(channel_id):
    if not API_KEY or not channel_id:
        print("⚠️ Missing API key or channel ID")
        return []

    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}"
        f"&channelId={channel_id}"
        "&part=snippet"
        "&order=date"
        "&maxResults=10"
    )

    try:
        res = requests.get(url).json()

        titles = []
        for item in res.get("items", []):
            if "snippet" in item:
                titles.append(item["snippet"]["title"])

        return titles

    except Exception as e:
        print("❌ YouTube API error:", e)
        return []