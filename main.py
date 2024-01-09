# main.py

import os
from flask import Flask
from flask_cors import CORS, cross_origin
from app.routes import query, faq, chatbot

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/query": {"origins": "*"},
        r"/faq": {"origins": "*"},
        r"/faqs": {"origins": "*"},
        r"/faq/<string:faq_id>": {"origins": "*"},
    },
)

app.config.from_object("app.config.Config")
app.register_blueprint(query.bp)
app.register_blueprint(faq.bp)
app.register_blueprint(chatbot.bp)

port = int(os.environ.get("PORT", 5000))


@app.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
