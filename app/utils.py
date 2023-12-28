from flask import jsonify


def generate_response(message, status, code, score=None):
    response = {} if score is None else {"score": score}
    response["message"] = message
    response["status"] = status
    return jsonify(response), code
