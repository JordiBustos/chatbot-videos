# main.py

import os
from flask import Flask
from app.routes.query import handle_response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "*"}})
app.config.from_object("app.config.Config")

port = int(os.environ.get("PORT", 5000))


@app.route("/query", methods=["GET"])
@cross_origin()
def main_route():
    return handle_response()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
