from PIL import Image

# 🔥 Fix for Pillow >= 10 (MoviePy compatibility)
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS
from moviepy.editor import *
import os


def estimate_duration(sentence):
    words = len(sentence.split())
    return max(1.5, words / 2.5)


def create_video(img_folder, audio_path, sentences):
    images = sorted([
        os.path.join(img_folder, i)
        for i in os.listdir(img_folder)
        if i.endswith(".jpg")
    ])

    voice = AudioFileClip(audio_path)

    clips = []
    total_time = 0

    for i, sentence in enumerate(sentences):
        if i >= len(images):
            break

        dur = estimate_duration(sentence)
        total_time += dur

        clip = (
            ImageClip(images[i])
            .set_duration(dur)
            .resize((1080, 1920))
        )

        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    # match audio
    video = video.set_audio(voice).set_duration(voice.duration)

    video.write_videofile(
        "output.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )