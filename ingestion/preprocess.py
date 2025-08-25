import re

def preprocess_data(data: list) -> list:
    """
    Cleans, normalizes, and tokenizes raw text data.
    """
    cleaned = []
    for item in data:
        if not item:
            continue
        text = item.get("text") if isinstance(item, dict) else str(item)
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)
        cleaned.append({"text": text, "meta": item.get("meta", {}) if isinstance(item, dict) else {}})
    return cleaned

def tokenize(text: str) -> list:
    """Simple whitespace tokenizer"""
    return text.split()

