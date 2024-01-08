from flask import jsonify
import re


def generate_response(message, status, code, score=None):
    response = {} if score is None else {"score": score}
    response["message"] = message
    response["status"] = status
    return jsonify(response), code


def has_no_letters(query):
    return not re.search(r"[a-zA-Z]", query)


def get_prompt(request):
    return request.args.get("prompt")


def validate_prompt(prompt):
    if prompt is None or not prompt.strip():
        return generate_response("El prompt es obligatorio", "error", 400)
    if has_no_letters(prompt):
        return generate_response(
            "El prompt ingresado es inválido. Debe contener letras", "error", 400
        )
    return True


def string_not_null(string):
    return string is not None and string.strip() != ""