from flask import Blueprint

blueprint = Blueprint(
    "eom blueprint", __name__, url_prefix="/eom"
)
