import random

def generate_titles(topic):
    return [
        f"Did you know {topic}",
        f"{topic} nobody talks about",
        f"This {topic} is insane",
        f"The hidden truth about {topic}"
    ]

def choose_best_title(titles):
    return titles[0]

def generate_hashtags(topic):
    words = topic.split()
    return ["#history","#facts","#viral"] + [f"#{w}" for w in words]