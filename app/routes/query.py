from flask import request
from app.services.qdrant_service import connect_qdrant, search_in_qdrant
from app.config import Config
from app.utils import generate_response


def handle_response():
    qdrant_client = connect_qdrant()
    if qdrant_client is None:
        return generate_response(
            "No se ha podido conectar al cliente de Qdrant", "error", 500
        )

    prompt = get_prompt(request)

    if prompt is None or prompt == "":
        return generate_response("El prompt es obligatorio", "error", 400)

    try:
        search_result = search_in_qdrant(prompt, Config.COLLECTION_NAME, qdrant_client)
        return handle_search_result(search_result)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_search_result(search_result):
    qdrant_search_errors = {
        "e": generate_response("Algo salió mal en la búsqueda", "error", 400),
        "ve": generate_response(
            "Input inválido. Asegúrese que el prompt ingresado existe", "error", 400
        ),
        "nre": generate_response(
            "No se han hallado resultados para la query.", "error", 404
        ),
    }

    return (
        process_successful_search(search_result)
        if isinstance(search_result, list)
        else qdrant_search_errors[search_result]
    )


def process_successful_search(search_result):
    score = search_result[0].score

    if score < Config.SCORE_THRESHOLD:
        return generate_response("No se han encontrado resultados", "error", 404)

    return generate_response(generate_yt_link(search_result[0]), "ok", 200, score)


def generate_yt_link(best_response):
    return (
        best_response.metadata["link"]
        + "&t="
        + str(best_response.metadata["start_time"])
        + "s"
    )


def get_prompt(request):
    return request.get_json().get("prompt")
