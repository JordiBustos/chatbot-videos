from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import Config
from app.utils import generate_response


class NoResultsError(Exception):
    pass


def connect_qdrant():
    try:
        qdrant_client = QdrantClient(
            url=Config.QDRANT_ENDPOINT,
            api_key=Config.QDRANT_KEY,
        )

        qdrant_client.set_model("intfloat/multilingual-e5-large")

        try:
            qdrant_client.get_collection(
                collection_name=Config.COLLECTION_NAME)
        except:
            qdrant_client.create_collection(
                collection_name=Config.COLLECTION_NAME_FAQ,
                vectors_config=models.VectorParams(
                    size=1024, distance=models.Distance.COSINE),
            )

        return qdrant_client
    except Exception as e:
        print(e)
        return None


def search_in_qdrant(query_text, collection_name, qdrant_client):
    try:
        if not query_text or not collection_name or not qdrant_client:
            raise ValueError(
                "Invalid input. Ensure query_text, collection_name, and qdrant_client are provided."
            )

        results = qdrant_client.query(collection_name, [query_text])
        if not results:
            raise NoResultsError(
                "No results found in Qdrant for the given query.")

        return results
    except ValueError as ve:
        return "ve"
    except NoResultsError as nre:
        return "nre"
    except Exception as e:
        return "e"


def get_qdrant_errors():
    return {
        "e": generate_response("Algo salió mal en la búsqueda", "error", 400),
        "ve": generate_response(
            "Input inválido. Asegúrese que el prompt ingresado existe", "error", 400
        ),
        "nre": generate_response(
            "No se han hallado resultados para la query.", "error", 404
        ),
    }
