from flask import Blueprint
from app.config import Config
from flask_cors import cross_origin

bp = Blueprint("chatbot", __name__)


@bp.route(f"{Config.API_VERSION}/chatbot", methods=["GET"])
@cross_origin()
def main_route():
    return "Hello World!"
