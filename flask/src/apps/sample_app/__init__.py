from flask import Blueprint

blueprint = Blueprint(
    "sample_app blueprint", __name__, url_prefix="/sample_app"
)
