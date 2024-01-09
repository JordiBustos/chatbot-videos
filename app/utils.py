from flask import jsonify
import re
from typing import Optional, Union, Tuple


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


def validate_prompt(prompt: str) -> Union[bool, Tuple[jsonify, float]]:
    if prompt is None or not prompt.strip():
        return generate_response("El prompt es obligatorio", "error", 400)
    if has_no_letters(prompt):
        return generate_response(
            "El prompt ingresado es inválido. Debe contener letras", "error", 400
        )
    return True


def string_not_null(string: str) -> bool:
    return string is not None and string.strip() != ""
