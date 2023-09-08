from flask import Blueprint

blueprint = Blueprint(
    "coin blueprint", __name__, url_prefix="/coin"
)
