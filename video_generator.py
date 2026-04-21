from PIL import Image

# Fix for Pillow 10+
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS
import os
import random
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


# ---------------------------
# 🎯 SETTINGS
# ---------------------------
WIDTH = 1080
HEIGHT = 1920
MIN_DURATION = 40
MAX_DURATION = 55


# ---------------------------
# 🧠 GET AUDIO DURATION
# ---------------------------
def get_audio_duration(audio_path):
    audio = AudioFileClip(audio_path)
    return audio.duration


# ---------------------------
# 🎞️ CREATE IMAGE CLIP
# ---------------------------
def create_clip(image_path, duration):

    clip = (
        ImageClip(image_path)
        .resize(height=HEIGHT)  # keep ratio
        .set_duration(duration)
    )

    # 🔥 Random zoom (Ken Burns effect)
    zoom = random.choice(["in", "out"])

    if zoom == "in":
        clip = clip.resize(lambda t: 1 + 0.08 * t)
    else:
        clip = clip.resize(lambda t: 1 + 0.08 * (duration - t))

    # center crop to 1080x1920
    clip = clip.crop(
        x_center=clip.w / 2,
        y_center=clip.h / 2,
        width=WIDTH,
        height=HEIGHT
    )

    return clip


# ---------------------------
# 🎬 MAIN VIDEO CREATOR
# ---------------------------
def create_video(image_folder, audio_path, sentences):

    print("🎬 Creating video...")

    images = sorted([
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.endswith(".jpg") or img.endswith(".png")
    ])

    if not images:
        raise Exception("❌ No images found")

    # ---------------------------
    # 🎧 LOAD AUDIO
    # ---------------------------
    audio = AudioFileClip(audio_path).set_fps(44100)
    audio_duration = audio.duration

    print(f"🎧 Audio duration: {audio_duration:.2f}s")

    # ---------------------------
    # ⏱️ FORCE MIN LENGTH
    # ---------------------------
    if audio_duration < MIN_DURATION:
        print("⚠️ Audio too short → looping")

        loops = int(MIN_DURATION // audio_duration) + 1
        audio = concatenate_videoclips([audio] * loops).audio
        audio_duration = audio.duration

    # ---------------------------
    # 🧠 SENTENCE TIMING
    # ---------------------------
    total_sentences = len(sentences)
    if total_sentences == 0:
        total_sentences = 1

    duration_per_sentence = audio_duration / total_sentences

    # ---------------------------
    # 🎞️ CREATE CLIPS
    # ---------------------------
    clips = []

    for i, sentence in enumerate(sentences):

        img = images[i % len(images)]

        clip = create_clip(img, duration_per_sentence)

        clips.append(clip)

    # ---------------------------
    # 🎬 MERGE
    # ---------------------------
    video = concatenate_videoclips(clips, method="compose")

    # ---------------------------
    # 🔊 SET AUDIO
    # ---------------------------
    video = video.set_audio(audio)

    # ---------------------------
    # ✂️ CUT TO MAX 55s
    # ---------------------------
    if video.duration > MAX_DURATION:
        video = video.subclip(0, MAX_DURATION)

    print(f"🎬 Final duration: {video.duration:.2f}s")

    # ---------------------------
    # 💾 EXPORT
    # ---------------------------
    video.write_videofile(
        "output.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="ultrafast"
    )

    print("✅ Video saved as output.mp4")
