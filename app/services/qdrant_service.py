from qdrant_client import QdrantClient
from app.config import Config


class NoResultsError(Exception):
    pass


def connect_qdrant():
    try:
        qdrant_client = QdrantClient(
            url=Config.QDRANT_ENDPOINT,
            api_key=Config.QDRANT_KEY,
        )

        qdrant_client.set_model("intfloat/multilingual-e5-large")

        return qdrant_client
    except Exception as e:
        return None


def search_in_qdrant(query_text, collection_name, qdrant_client):
    try:
        if not query_text or not collection_name or not qdrant_client:
            raise ValueError(
                "Invalid input. Ensure query_text, collection_name, and qdrant_client are provided."
            )

        results = qdrant_client.query(collection_name, [query_text])
        if not results:
            raise NoResultsError("No results found in Qdrant for the given query.")

        return results
    except ValueError as ve:
        return "ve"
    except NoResultsError as nre:
        return "nre"
    except Exception as e:
        return "e"
