"""
Thin wrapper around the Hugging Face sentiment-analysis pipeline.

Kept separate from main.py so the model-loading logic can be unit
tested / swapped independently of the HTTP layer, and so the
Jenkins "model eval gate" stage can import just this module.
"""
from functools import lru_cache
from transformers import pipeline

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"


@lru_cache(maxsize=1)
def get_pipeline():
    """Load the model once per process and cache it."""
    return pipeline("sentiment-analysis", model=MODEL_NAME)


def predict(text: str) -> dict:
    """
    Run sentiment analysis on a single piece of text.

    Returns a dict like: {"label": "POSITIVE", "score": 0.9998}
    """
    if not text or not text.strip():
        raise ValueError("text must be a non-empty string")

    clf = get_pipeline()
    result = clf(text[:512])[0]  # DistilBERT's max context is small; truncate defensively
    return {"label": result["label"], "score": round(float(result["score"]), 4)}
