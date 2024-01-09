from flask import jsonify
import re
from typing import Optional, Union, Tuple
from app.config import Config


def generate_response(
    message: Union[str, list, dict],
    status: str,
    code: int,
    score: Optional[float] = None,
) -> Tuple[dict, float]:
    response = {} if score is None else {"score": score}
    response["message"] = message
    response["status"] = status
    return jsonify(response), code


def has_no_letters(query: str) -> bool:
    return not re.search(r"[a-zA-Z]", query)


def get_prompt(request: dict) -> str:
    return request.args.get("prompt")


def validate_prompt(prompt: str) -> Union[bool, Tuple[dict, float]]:
    if prompt is None or not prompt.strip():
        return generate_response("El prompt es obligatorio", "error", 400)
    if has_no_letters(prompt):
        return generate_response(
            "El prompt ingresado es inválido. Debe contener letras", "error", 400
        )
    return True


def string_not_null(string: str) -> bool:
    return string is not None and string.strip() != ""


def process_successful_search(search_result):
    score = search_result[0].score
    if score < Config.SCORE_THRESHOLD:
        return generate_response("No se han encontrado resultados", "error", 404)
    return generate_response(search_result[0].metadata["answer"], "ok", 200, score)


def generate_faq_dict(doc: dict, doc_id: int) -> dict:
    return {
        "id": doc_id,
        "question": doc["document"],
        "answer": doc["answer"],
        "category": doc["category"],
        "courses_id": doc["courses_id"],
    }
