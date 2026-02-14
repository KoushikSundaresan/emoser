import random

EMOTION_CLUSTERS = {
    "calm": ["calm", "peaceful", "relaxed", "grounded", "serene"],
    "joy": ["happy", "energized", "excited", "playful", "radiant"],
    "love": ["caring", "warm", "connected", "affectionate", "tender"],
    "confident": ["capable", "strong", "worthy", "proud", "determined"],
    "sad": ["lonely", "down", "discouraged", "heavy-hearted", "weary"],
    "anxious": ["uneasy", "nervous", "worried", "on edge", "tense"],
    "angry": ["irritated", "frustrated", "resentful", "bitter"],
    "numb": ["empty", "distant", "withdrawn", "shut down"]
}

BODY_CLUSTERS = {
    "tense": ["tight", "rigid", "clenched", "constricted"],
    "heavy": ["heavy", "slow", "drained", "weighed down"],
    "restless": ["jittery", "fluttery", "shaky", "buzzy"],
    "numb": ["numb", "hollow", "spacey", "disconnected"],
    "warm": ["soft", "loose", "warm", "settled"]
}

def pick_word(cluster_dict, key):
    return random.choice(cluster_dict[key])
