from flask import Flask
from importlib import import_module


def create_app():
    app = Flask(__name__)

    # blueprints

    for module_name in [
        "sample_app",
        "weather",
        "coin",
        "file_uploader",
        "crawler",
        "market",
    ]:
        module = import_module(f"apps.{module_name}.routes")
        app.register_blueprint(module.blueprint)

    return app
