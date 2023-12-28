from flask import jsonify
import re


def generate_response(message, status, code, score=None):
    response = {} if score is None else {"score": score}
    response["message"] = message
    response["status"] = status
    return jsonify(response), code


def has_no_letters(query):
    return not re.search(r"[a-zA-Z]", query)
