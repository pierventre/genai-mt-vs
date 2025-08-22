def preprocess(doc: dict) -> dict:
    text = doc["content"].replace("\r", " ").replace("\n", " ").strip()
    text = " ".join(text.split())  # collapse whitespace
    return {**doc, "cleaned": text, "lang": "en"}  # keep it simple for demo
