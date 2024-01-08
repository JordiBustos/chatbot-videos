# main.py

import os
from flask import Flask
from app.routes.query import handle_query_response
from app.routes.faq import handle_faq_response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "*"}})
app.config.from_object("app.config.Config")

port = int(os.environ.get("PORT", 5000))

API_VERSION = "/api/v1"

@app.route(API_VERSION + "/query", methods=["GET"])
@cross_origin()
def main_route():
    return handle_query_response()


@app.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    return "OK", 200


@app.route(API_VERSION + "/faq", methods=["GET", "POST"])
@cross_origin()
def add_faq():
    return handle_faq_response()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
