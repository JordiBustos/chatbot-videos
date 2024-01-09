from flask import Blueprint
from app.config import Config
from flask_cors import cross_origin
from app.controllers.query import handle_query_response

bp = Blueprint("query", __name__)


@bp.route(f"{Config.API_VERSION}/query", methods=["GET"])
@cross_origin()
def main_route():
    return handle_query_response()
