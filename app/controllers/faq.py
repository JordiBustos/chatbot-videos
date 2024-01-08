from typing import Tuple, Union
from flask import request
from qdrant_client import QdrantClient
from app.services.qdrant_service import connect_qdrant, search_in_qdrant
from app.config import Config
from app.utils import generate_response, get_prompt, validate_prompt, string_not_null


def handle_faq_response(all: bool =False) -> dict:
    if (request.method == "GET"):
        return handle_get_response() if not all else handle_get_all_response()
    if (request.method == "POST"):
        return handle_post_response()
    return generate_response("Método no permitido", "error", 405)


def handle_get_all_response() -> dict:
    conn: Union[Tuple[QdrantClient, bool], Tuple[Tuple[dict, int], bool]] = connect_qdrant()
    if not conn[1]:
        return conn[0]
    qdrant_client: QdrantClient = conn[0]
    try:
        records: list = qdrant_client.scroll(
            collection_name=Config.COLLECTION_NAME_FAQ, limit=1000
        )[0]
        response: list[dict] = []
        for doc in records:
            response.append({
                "id":doc.id,
                "question": doc.payload["document"],
                "answer": doc.payload["answer"],
                "category": doc.payload["category"],
                "courses_id": doc.payload["courses_id"]
            })
        return generate_response(response, "ok", 200)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_get_response():
    prompt: str = get_prompt(request)
    prompt_validation: Union[bool, Tuple[any, float]] = validate_prompt(prompt)
    if (prompt_validation is not True):
        return prompt_validation
    conn: Union[Tuple[QdrantClient, bool], Tuple[Tuple[dict, int], bool]] = connect_qdrant()
    if not conn[1]:
        return conn[0]
    qdrant_client: QdrantClient = conn[0]
    try:
        search_result: Union[list, str] = search_in_qdrant(
            prompt, Config.COLLECTION_NAME_FAQ, qdrant_client)
        return handle_faq_result(search_result)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_post_response():
    question: str = request.form["question"]
    answer: str = request.form["answer"]
    category: str = request.form["category"]
    courses_id: list[str] = request.form.getlist("courses_id")

    if (not string_not_null(question)):
        return generate_response("La pregunta es obligatoria", "error", 400)
    if (not string_not_null(answer)):
        return generate_response("La respuesta es obligatoria", "error", 400)
    if (not string_not_null(category)):
        return generate_response("La categoría es obligatoria", "error", 400)

    conn: Union[Tuple[QdrantClient, bool], Tuple[Tuple[dict, int], bool]] = connect_qdrant()
    if not conn[1]:
        return conn[0]
    qdrant_client: QdrantClient = conn[0]
    md: dict = {
        "answer": answer,
        "category": category,
        "courses_id": courses_id
    }
    text: str = question.strip()

    try:
        qdrant_client.add(Config.COLLECTION_NAME_FAQ,
                          documents=[text], metadata=[md])
        return generate_response("Pregunta agregada correctamente", "ok", 200)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_faq_result(search_result):
    return (
        process_successful_search(search_result)
        if isinstance(search_result, list)
        else search_result
    )


def process_successful_search(search_result):
    score = search_result[0].score
    if score < Config.SCORE_THRESHOLD:
        return generate_response("No se han encontrado resultados", "error", 404)
    return generate_response(search_result[0].metadata["answer"], "ok", 200, score)


def update_or_delete_faq(faq_id: str):
    return generate_response("Método no permitido", "error", 405)