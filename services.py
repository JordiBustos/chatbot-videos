import os
from flask import Flask, jsonify, request
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()
COLLECTION_NAME = "demo"
SCORE_THRESHOLD = 0.85

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))


class NoResultsError(Exception):
    pass


def connect_qdrant():
    try:
        qdrant_client = QdrantClient(
            url=os.environ.get("QDRANT_ENDPOINT"),
            api_key=os.environ.get("QDRANT_KEY"),
        )

        qdrant_client.set_model("intfloat/multilingual-e5-large")

        return qdrant_client
    except:
        return None


def search_in_qdrant(query_text, collection_name, qdrant_client):
    try:
        if (not query_text or not collection_name or not qdrant_client):
            raise ValueError(
                "Invalid input. Ensure query_text, collection_name, and qdrant_client are provided.")

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
        return None


def handle_search_result(search_result):
    errors = {
        None: (jsonify({"error": "Algo salió mal en la búsqueda", "status": "error"}), 400),
        "ve": (jsonify({"error": "Input inválido. Asegúrese que query_text, collection_name y qdrant_client existen", "status": "error"}), 400),
        "nre": (jsonify({"error": "No se han hallado resultados para la query.", "status": "error"}), 404)
    }
    return process_successful_search(search_result) if isinstance(search_result, list) else errors[search_result]


def process_successful_search(search_result):
    score = search_result[0].score

    if score <= SCORE_THRESHOLD:
        return jsonify({"message": "No se han encontrado resultados", "status": "error"}), 404

    answer = (
        search_result[0].metadata["link"]
        + "&t="
        + str(search_result[0].metadata["start_time"])
        + "s"
    )
    return jsonify({
        'message': answer,
        "score": score,
        "status": "ok"
    }), 200


@app.route('/query', methods=['GET'])
def generate_response():
    qdrant_client = connect_qdrant()
    qdrant_connection_error = jsonify(
        {"error": "No se ha podido conectar al cliente de Qdrant", "status": "error"}), 500

    if qdrant_client is None:
        return qdrant_connection_error

    data = request.json
    prompt = data.get("prompt")

    if (prompt is None or prompt == ''):
        return jsonify({"error": "El prompt es obligatorio", "status": "error"}), 400

    search_result = search_in_qdrant(prompt, COLLECTION_NAME, qdrant_client)
    return handle_search_result(search_result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
