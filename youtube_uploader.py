import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


# ---------------------------
# LOAD TOKEN
# ---------------------------
def get_credentials():
    if not os.path.exists("token.json"):
        raise Exception("❌ Run auth.py first to generate token.json")

    return Credentials.from_authorized_user_file("token.json", SCOPES)


# ---------------------------
# SAFE TITLE HANDLER
# ---------------------------
def safe_title(title):
    if not title or len(title.strip()) == 0:
        return "😱 Viral Fact You Didn't Know #shorts"

    title = title.strip()

    if len(title) > 100:
        title = title[:100]

    return title


# ---------------------------
# UPLOAD VIDEO
# ---------------------------
def upload_video(title, description, thumbnail_path=None):
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    title = safe_title(title)

    if not description or len(description.strip()) == 0:
        description = "#shorts #viral"

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": description.split()
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload("output.mp4")
    )

    response = request.execute()
    video_id = response["id"]

    # ---------------------------
    # THUMBNAIL UPLOAD
    # ---------------------------
    if thumbnail_path and os.path.exists(thumbnail_path):
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()

    return f"https://youtube.com/watch?v={video_id}"