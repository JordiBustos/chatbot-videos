from flask import Blueprint
from app.config import Config
from app.controllers.faq import handle_faq_response, update_or_delete_faq
from flask_cors import cross_origin


bp = Blueprint("faq", __name__)


@bp.route(f"{Config.API_VERSION}/faq", methods=["GET", "POST"])
@cross_origin()
def faq():
    return handle_faq_response()


@bp.route(f"{Config.API_VERSION}/faqs", methods=["GET"])
@cross_origin()
def faqs():
    return handle_faq_response(all=True)


# TODO
@bp.route(f"{Config.API_VERSION}/faq/<string:faq_id>", methods=["GET", "PUT", "DELETE"])
@cross_origin()
def update_faq(faq_id):
    return update_or_delete_faq(faq_id)
