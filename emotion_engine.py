# support running both as part of the emoser package and as a standalone script
try:
    from .data import EMOTION_CLUSTERS, pick_word
except ImportError:
    # when main.py is executed directly, __package__ may be None and relative
    # imports will fail; fall back to absolute module path (works because the
    # package directory is added to sys.path in main.py's import logic).
    from data import EMOTION_CLUSTERS, pick_word

WEIGHTS = {
    "greatly_agree": 4,
    "agree": 2,
    "neutral": 0,
    "disagree": -1,
    "greatly_disagree": -2
}

def new_score():
    return {k: 0 for k in EMOTION_CLUSTERS.keys()}

def apply(score, answer, mapping):
    w = WEIGHTS[answer]
    for cluster, factor in mapping.items():
        score[cluster] += w * factor

def detect_emotions(answers):
    score = new_score()

    questions = [
        {"sad":1, "numb":1, "anxious":0.5},
        {"anxious":1, "angry":0.5, "numb":-0.5},
        {"numb":1, "sad":0.5, "love":-0.5},
        {"angry":1, "anxious":0.5, "calm":-1},
        {"joy":1, "confident":0.5, "sad":-1},
        {"love":1, "calm":0.5, "numb":-1},
        {"confident":1, "calm":0.5, "anxious":-1},
        {"anxious":1, "sad":0.5, "numb":0.5},
        {"sad":1, "numb":0.5, "joy":-1},
        {"joy":1, "love":0.5, "confident":0.5}
    ]

    for ans, mapping in zip(answers, questions):
        apply(score, ans, mapping)

    top = sorted(score, key=score.get, reverse=True)[:2]
    return [pick_word(EMOTION_CLUSTERS, t) for t in top]
