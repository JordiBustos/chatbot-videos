# main.py

import os
from flask import Flask
from app.routes.query import generate_response

app = Flask(__name__)
app.config.from_object("app.config.Config")

port = int(os.environ.get("PORT", 5000))


@app.route("/query", methods=["GET"])
def main_route():
    return generate_response()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
