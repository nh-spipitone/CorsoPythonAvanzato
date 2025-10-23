from flask import Flask
from app.utils import db, jwt
from app.config import config


TESTING: bool = True

app = Flask(__name__)

# Configuration from env
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["PROPAGATE_EXCEPTIONS"] = True
if TESTING:
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

from .routes.recipes import recipes_bp

app.register_blueprint(recipes_bp)

db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()
