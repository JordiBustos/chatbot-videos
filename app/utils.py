from flask import jsonify
import re
from typing import Optional, Union
from app.config import Config
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client import QdrantClient
from app.types import Response, FaqDict


def generate_response(
    message: Union[str, list, dict],
    status: str,
    code: int,
    score: Optional[float] = None,
) -> Response:
    response = {} if score is None else {"score": score}
    response["message"] = message
    response["status"] = status
    return jsonify(response), code


def has_no_letters(query: str) -> bool:
    return not re.search(r"[a-zA-Z]", query)


def get_prompt(request: dict) -> str:
    return request.args.get("prompt")


def validate_prompt(prompt: str) -> Union[bool, Response]:
    if prompt is None or not prompt.strip():
        return generate_response("El prompt es obligatorio", "error", 400)
    if has_no_letters(prompt):
        return generate_response(
            "El prompt ingresado es inválido. Debe contener letras", "error", 400
        )
    return True


def string_not_null(string: str) -> bool:
    return string is not None and string.strip() != ""


def process_successful_search(search_result: list) -> Response:
    score = search_result[0].score
    if score < Config.SCORE_THRESHOLD:
        return generate_response("No se han encontrado resultados", "error", 404)
    return generate_response(search_result[0].metadata["answer"], "ok", 200, score)


def generate_faq_dict(doc: dict, doc_id: int) -> FaqDict:
    return {
        "id": doc_id,
        "question": doc["document"],
        "answer": doc["answer"],
        "category": doc["category"],
        "courses_id": doc["courses_id"],
    }


def retrieve_faq(qdrant_client: QdrantClient, faq_id: str) -> Union[Response, tuple]:
    try:
        faq = qdrant_client.retrieve(Config.COLLECTION_NAME_FAQ, [faq_id])
        return faq, False
    except UnexpectedResponse as ue:
        return generate_response(f"{ue}", "error", 404), True
    except Exception as e:
        return generate_response(f"{e}", "error", 500), True
