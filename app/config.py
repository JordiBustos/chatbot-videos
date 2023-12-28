import os
from app.utils import generate_response


class Config:
    COLLECTION_NAME = "demo"
    SCORE_THRESHOLD = 0.85
    QDRANT_ENDPOINT = os.environ.get("QDRANT_ENDPOINT")
    QDRANT_KEY = os.environ.get("QDRANT_KEY")
