import os


class Config:
    COLLECTION_NAME = "demo"
    COLLECTION_NAME_FAQ = "faq"
    SCORE_THRESHOLD = 0.85
    QDRANT_ENDPOINT = os.environ.get("QDRANT_ENDPOINT")
    QDRANT_KEY = os.environ.get("QDRANT_KEY")
