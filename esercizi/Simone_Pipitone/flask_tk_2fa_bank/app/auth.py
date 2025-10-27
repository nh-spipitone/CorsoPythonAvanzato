import pyotp
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from . import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/login")
def login():
    # Se già loggato vai alla dashboard
    if session.get("user_id"):
        return redirect(url_for("bank.dashboard"))
    return render_template("login.html")

@bp.post("/login")
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        flash("Inserisci username e password", "error")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        flash("Credenziali non valide", "error")
        return redirect(url_for("auth.login"))
    # Passo 1 OK → richiedi OTP
    session["pending_user_id"] = user.id
    return redirect(url_for("auth.otp"))

@bp.get("/otp")
def otp():
    if not session.get("pending_user_id"):
        return redirect(url_for("auth.login"))
    return render_template("otp.html")

@bp.post("/otp")
def otp_post():
    if not session.get("pending_user_id"):
        return redirect(url_for("auth.login"))
    code = request.form.get("code", "").strip()
    user = User.query.get(session["pending_user_id"])
    if not user:
        return redirect(url_for("auth.login"))
    totp = pyotp.TOTP(user.totp_secret)
    if not code or not totp.verify(code, valid_window=1):
        flash("OTP non valido o scaduto", "error")
        return redirect(url_for("auth.otp"))
    # Login completato
    session.pop("pending_user_id", None)
    session["user_id"] = user.id
    flash("Accesso eseguito", "success")
    return redirect(url_for("bank.dashboard"))

@bp.get("/logout")
def logout():
    session.clear()
    flash("Sei uscito", "info")
    return redirect(url_for("auth.login"))
