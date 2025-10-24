import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://app:app@localhost:5432/appdb"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from .models import User, Account, Tx
        db.create_all()

        if os.getenv("CREATE_DEMO_USER", "1") == "1":
            from werkzeug.security import generate_password_hash
            username = os.getenv("DEMO_USERNAME", "student")
            password = os.getenv("DEMO_PASSWORD", "password123")
            secret = os.getenv("DEMO_TOTP_SECRET", "JBSWY3DPEHPK3PXP")
            u = User.query.filter_by(username=username).first()
            if not u:
                u = User(username=username, password_hash=generate_password_hash(password), totp_secret=secret)
                db.session.add(u)
                db.session.commit()
                acct = Account(user_id=u.id, balance=1000_00)  # centesimi
                db.session.add(acct)
                db.session.commit()

    from .auth import bp as auth_bp
    from .bank import bp as bank_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(bank_bp)

    @app.get("/")
    def index():
        # reindirizza in base allo stato di login
        from flask import session
        if session.get("user_id"):
            return redirect(url_for("bank.dashboard"))
        return redirect(url_for("auth.login"))

    return app

# entrypoint per `flask --app app run`
app = create_app()
