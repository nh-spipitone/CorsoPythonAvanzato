from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .task import bp
    app.register_blueprint(bp)
    return app
