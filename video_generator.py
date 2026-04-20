# ---------------------------
# PIL FIX (IMPORTANT)
# ---------------------------
from PIL import Image

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


# ---------------------------
# IMPORTS
# ---------------------------
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    ColorClip
)

import os


# ---------------------------
# SAFE DURATION ESTIMATION
# ---------------------------
def estimate_duration(sentence):
    words = len(sentence.split())
    return max(1.2, min(4, words / 2.8))


# ---------------------------
# SAFE IMAGE LOADER
# ---------------------------
def safe_image(path):
    try:
        return ImageClip(path)
    except Exception as e:
        print(f"⚠️ Bad image skipped: {path}")
        return None


# ---------------------------
# CREATE VIDEO
# ---------------------------
def create_video(img_folder, audio_path, sentences):

    # ---------------------------
    # LOAD AUDIO (FIXED)
    # ---------------------------
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
        raise Exception("❌ Invalid audio file")

    voice = AudioFileClip(audio_path).set_fps(44100)

    # ---------------------------
    # LOAD IMAGES
    # ---------------------------
    images = sorted([
        os.path.join(img_folder, i)
        for i in os.listdir(img_folder)
        if i.endswith((".jpg", ".png"))
    ])

    clips = []

    # ---------------------------
    # FALLBACK (NO IMAGES)
    # ---------------------------
    if not images:
        print("⚠️ No images → black background")

        clip = ColorClip((720, 1280), color=(0, 0, 0)) \
            .set_duration(voice.duration) \
            .set_audio(voice)

        clip.write_videofile(
            "output.mp4",
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=2
        )
        return

    # ---------------------------
    # LIMIT CLIPS (PREVENT RAM CRASH)
    # ---------------------------
    max_clips = min(len(sentences), len(images), 15)

    for i in range(max_clips):

        dur = estimate_duration(sentences[i])

        clip = safe_image(images[i])
        if clip is None:
            continue

        try:
            clip = (
                clip
                .set_duration(dur)
                .resize(height=1280)
                .set_position("center")
            )

            clips.append(clip)

        except Exception as e:
            print(f"⚠️ Clip error: {e}")

    # ---------------------------
    # SAFETY CHECK
    # ---------------------------
    if not clips:
        raise Exception("❌ No valid clips")

    # ---------------------------
    # CONCAT VIDEO (SAFE)
    # ---------------------------
    try:
        video = concatenate_videoclips(clips, method="compose")
    except Exception as e:
        print("⚠️ concat failed, using first clip")
        video = clips[0]

    # ---------------------------
    # 🔥 CRITICAL AUDIO FIX
    # ---------------------------
    video = video.set_audio(voice)

    # match duration EXACTLY
    video = video.set_duration(voice.duration)

    # ---------------------------
    # EXPORT VIDEO (STABLE)
    # ---------------------------
    video.write_videofile(
        "output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2,
        audio_fps=44100
    )
