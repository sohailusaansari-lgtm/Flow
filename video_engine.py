from moviepy.editor import *
import requests
from PIL import Image
from io import BytesIO

def create_video(title, idea):
    img = Image.open(BytesIO(requests.get(
        f"https://image.pollinations.ai/prompt/{idea} 4k"
    ).content))

    img.save("frame.jpg")

    clip = ImageClip("frame.jpg").set_duration(6)
    txt = TextClip(title, fontsize=60, color='white').set_duration(6)

    video = CompositeVideoClip([clip, txt])
    video.write_videofile("output.mp4", fps=24)

    return "output.mp4"