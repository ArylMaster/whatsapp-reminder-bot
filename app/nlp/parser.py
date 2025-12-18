import spacy
import dateparser
from typing import Optional, Tuple
from datetime import datetime

# Load once at import time
nlp = spacy.load("en_core_web_sm")

FILLER_PHRASES = [
    "remind me to",
    "remind me",
    "please remind me to",
    "please remind me",
    "can you remind me to",
    "can you remind me",
]


from dateparser.search import search_dates


def extract_time(text: str) -> Optional[datetime]:
    results = search_dates(
        text,
        settings={
            "TIMEZONE": "Asia/Kolkata",
            "RETURN_AS_TIMEZONE_AWARE": False,
            "PREFER_DATES_FROM": "future",
        },
    )

    if not results:
        return None

    # results = [(matched_text, datetime), ...]
    return results[0][1]



def clean_message(text: str) -> str:
    lowered = text.lower()
    for phrase in FILLER_PHRASES:
        if lowered.startswith(phrase):
            return text[len(phrase):].strip()
    return text.strip()


def extract_message(text: str) -> str:
    """
    Extract the core action phrase using spaCy.
    """
    doc = nlp(text)

    root = next((token for token in doc if token.dep_ == "ROOT"), None)
    if not root:
        return clean_message(text)

    tokens = [root.text]

    for child in root.children:
        if child.dep_ in ("dobj", "prep", "attr", "pobj"):
            tokens.append(child.text)

    return clean_message(" ".join(tokens))


def parse_reminder(text: str):
    dt = extract_time(text)

    if not dt:
        return None, None

    message = extract_message(text)

    # Fallback: if NLP fails, use cleaned raw text
    if not message:
        message = clean_message(text)

    # Absolute fallback (never return None message)
    if not message.strip():
        message = "Reminder"

    return message, dt

