from flask import Blueprint
from app.config import Config
from app.controllers.faq import handle_faq_response
from flask_cors import cross_origin


bp = Blueprint("faq", __name__)


@bp.route(Config.API_VERSION + "/faq", methods=["GET", "POST"])
@cross_origin()
def faq():
    return handle_faq_response()
