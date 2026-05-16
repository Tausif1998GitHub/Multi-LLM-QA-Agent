import re


def analyze_sentiment(transcript):

    negative_words = [
        "frustrated",
        "angry",
        "bad",
        "terrible",
        "wait"
    ]

    score = 0

    for word in negative_words:
        score += transcript.lower().count(word)

    if score >= 2:
        return "frustrated"

    return "neutral"


def detect_policy_violations(transcript, policies):

    violations = []

    if "callback" not in transcript.lower():
        violations.append("No callback offered")

    if "thank you" not in transcript.lower():
        violations.append("No closing gratitude")

    return violations