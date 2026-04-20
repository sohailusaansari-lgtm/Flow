# ---------------------------
# PIL FIX (VERY IMPORTANT)
# ---------------------------
from PIL import Image

# Fix for Pillow >= 10 (MoviePy compatibility)
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


# ---------------------------
# IMPORTS
# ---------------------------
from moviepy.editor import *
import os


# ---------------------------
# ESTIMATE DURATION PER SENTENCE
# ---------------------------
def estimate_duration(sentence):
    words = len(sentence.split())
    return max(1.5, words / 2.5)  # natural speaking speed


# ---------------------------
# CREATE VIDEO
# ---------------------------
def create_video(img_folder, audio_path, sentences):

    # ---------------------------
    # LOAD IMAGES
    # ---------------------------
    images = sorted([
        os.path.join(img_folder, i)
        for i in os.listdir(img_folder)
        if i.endswith(".jpg") or i.endswith(".png")
    ])

    # ---------------------------
    # AUDIO
    # ---------------------------
    voice = AudioFileClip(audio_path)

    clips = []

    # ---------------------------
    # FALLBACK IF NO IMAGES
    # ---------------------------
    if not images:
        print("⚠️ No images found → using black background")

        clip = ColorClip(size=(1080, 1920), color=(0, 0, 0))
        clip = clip.set_duration(voice.duration)

        video = clip.set_audio(voice)

        video.write_videofile(
            "output.mp4",
            fps=30,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=2
        )
        return

    # ---------------------------
    # CREATE CLIPS PER SENTENCE
    # ---------------------------
    for i, sentence in enumerate(sentences):

        if i >= len(images):
            break

        dur = estimate_duration(sentence)

        img_path = images[i]

        try:
            clip = (
                ImageClip(img_path)
                .set_duration(dur)
                .resize((1080, 1920))
                .resize(lambda t: 1 + 0.05 * t)  # 🔥 zoom effect
                .set_position("center")
            )

            clips.append(clip)

        except Exception as e:
            print(f"⚠️ Skipping image {img_path}: {e}")

    # ---------------------------
    # SAFETY CHECK
    # ---------------------------
    if not clips:
        raise Exception("❌ No clips generated")

    # ---------------------------
    # CONCAT VIDEO
    # ---------------------------
    video = concatenate_videoclips(clips, method="compose")

    # ---------------------------
    # SYNC AUDIO
    # ---------------------------
    video = video.set_audio(voice).set_duration(voice.duration)

    # ---------------------------
    # EXPORT VIDEO
    # ---------------------------
    video.write_videofile(
        "output.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",  # 🔥 fast render
        threads=2
    )
