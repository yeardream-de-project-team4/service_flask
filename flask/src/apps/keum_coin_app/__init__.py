from flask import Blueprint

blueprint = Blueprint(
    "sample_app blueprint", __name__, url_prefix="/keum_coin_app"
)
