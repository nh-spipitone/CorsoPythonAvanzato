from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
import pyotp

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class BankUser(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    secret_key: Mapped[str] = mapped_column(nullable=False)

    def __init__(
        self, *, id: int | None = None, username: str, password: str, secret_key: str
    ) -> None:
        super().__init__()
        if id is not None:
            self.id = id
        self.username = username
        self.password = password
        self.secret_key = secret_key


def populate_db() -> None:
    if BankUser.query.first() is not None:
        return
    user = BankUser(
        username="mario",
        password=generate_password_hash("napoli1"),
        secret_key="cambiami",
    )
    db.session.add(user)
    db.session.commit()


with app.app_context():
    db.create_all()
    populate_db()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/login")
def login():
    return render_template("login.html")


@app.post("/login")
def auth():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = BankUser.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session["pending_userid"] = user.id
        session.pop("userid", None)
        return redirect(url_for("otp"))

    flash("credenziali non valide", "error")
    return redirect(url_for("login"))


@app.get("/otp")
def otp():
    pending_id = session.get("pending_userid")
    if not pending_id:
        return redirect(url_for("login"))

    if not BankUser.query.get(pending_id):
        session.pop("pending_userid", None)
        flash("utente non trovato", "error")
        return redirect(url_for("login"))

    return render_template("otp.html")


@app.post("/otp")
def otp_post():
    pending_id = session.get("pending_userid")
    if not pending_id:
        flash("autenticazione fallita", "error")
        return redirect(url_for("login"))

    user = BankUser.query.get(pending_id)
    if not user:
        session.pop("pending_userid", None)
        flash("utente non trovato", "error")
        return redirect(url_for("login"))

    code = request.form.get("code", "").strip()
    totp = pyotp.TOTP(user.secret_key)

    if not code or not totp.verify(code, valid_window=1):
        flash("OTP non valido o scaduto", "error")
        return redirect(url_for("otp"))

    flash("autenticazione riuscita", "success")
    session["userid"] = user.id
    session.pop("pending_userid", None)
    return redirect(url_for("index"))
