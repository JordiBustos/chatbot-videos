import os


class Config:
    COLLECTION_NAME: str = "demo"
    COLLECTION_NAME_FAQ: str = "faq"
    API_VERSION: str = "/api/v1"
    SCORE_THRESHOLD: float = 0.85
    EMBEDDING_MODEL_SIZE: int = 1024
    QDRANT_ENDPOINT: str = os.environ.get("QDRANT_ENDPOINT")
    QDRANT_KEY: str = os.environ.get("QDRANT_KEY")
