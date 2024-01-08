import os


class Config:
    COLLECTION_NAME = "demo"
    COLLECTION_NAME_FAQ = "faq"
    API_VERSION = "/api/v1"
    SCORE_THRESHOLD = 0.85
    EMBEDDING_MODEL_SIZE = 1024
    QDRANT_ENDPOINT = os.environ.get("QDRANT_ENDPOINT")
    QDRANT_KEY = os.environ.get("QDRANT_KEY")
