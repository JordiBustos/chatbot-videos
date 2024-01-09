from flask import request
from app.services.qdrant_service import (
    connect_qdrant,
    search_in_qdrant,
    get_qdrant_errors,
)
from app.config import Config
from app.types import QdrantError
from app.utils import generate_response, get_prompt, validate_prompt


def handle_query_response():
    prompt: str = get_prompt(request)

    prompt_validation = validate_prompt(prompt)
    if prompt_validation is not True:
        return prompt_validation

    qdrant_client, err = connect_qdrant()
    if err:
        return qdrant_client

    try:
        search_result = search_in_qdrant(prompt, Config.COLLECTION_NAME, qdrant_client)
        return handle_search_result(search_result)
    except Exception as e:
        return generate_response(f"{e}", "error", 500)


def handle_search_result(search_result):
    qdrant_search_errors: QdrantError = get_qdrant_errors()

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


def generate_yt_link(best_response: dict) -> str:
    return f"{best_response.metadata['link']}&t={str(best_response.metadata['start_time'])}s"
