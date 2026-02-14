# make imports resilient to script- versus package-based execution
try:
    from .data import BODY_CLUSTERS, pick_word
except ImportError:
    from data import BODY_CLUSTERS, pick_word
try:
    from .emotion_engine import WEIGHTS
except ImportError:
    from emotion_engine import WEIGHTS

def new_score():
    return {k: 0 for k in BODY_CLUSTERS.keys()}

def apply(score, answer, mapping):
    w = WEIGHTS[answer]
    for cluster, factor in mapping.items():
        score[cluster] += w * factor

def detect_body(answers):
    score = new_score()

    questions = [
        {"tense":1, "restless":0.5, "warm":-1},
        {"heavy":1, "numb":0.5, "restless":-0.5},
        {"restless":1, "tense":0.5, "heavy":-0.5},
        {"numb":1, "heavy":0.5, "warm":-1},
        {"warm":1, "tense":-1, "restless":-0.5},
        {"tense":1, "restless":0.5},
        {"heavy":1, "numb":0.5, "warm":-0.5}
    ]

    for ans, mapping in zip(answers, questions):
        apply(score, ans, mapping)

    top = max(score, key=score.get)
    return pick_word(BODY_CLUSTERS, top)
