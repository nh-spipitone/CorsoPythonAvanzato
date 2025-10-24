from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import select
from . import db
from .models import User, Account, Tx

bp = Blueprint("bank", __name__, url_prefix="")

def require_login():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)

def parse_amount_to_cents(s: str) -> int:
    s = (s or "").replace(",", ".").strip()
    try:
        val = float(s)
    except ValueError:
        return -1
    cents = int(round(val * 100))
    return cents

@bp.get("/dashboard")
def dashboard():
    user = require_login()
    if not user:
        return redirect(url_for("auth.login"))
    acct = user.account
    # Preleva ultime 10 transazioni
    txs = acct.txs[:10] if acct and acct.txs else []
    return render_template("dashboard.html", user=user, acct=acct, txs=txs)

@bp.post("/deposit")
def deposit():
    user = require_login()
    if not user:
        return redirect(url_for("auth.login"))
    amount = parse_amount_to_cents(request.form.get("amount"))
    if amount <= 0:
        flash("Importo non valido", "error")
        return redirect(url_for("bank.dashboard"))
    acct = user.account
    acct.balance += amount
    db.session.add(Tx(account_id=acct.id, kind="DEPOSIT", amount=amount, note="Deposito"))
    db.session.commit()
    flash("Deposito eseguito", "success")
    return redirect(url_for("bank.dashboard"))

@bp.post("/withdraw")
def withdraw():
    user = require_login()
    if not user:
        return redirect(url_for("auth.login"))
    amount = parse_amount_to_cents(request.form.get("amount"))
    acct = user.account
    if amount <= 0 or amount > acct.balance:
        flash("Importo non valido o fondi insufficienti", "error")
        return redirect(url_for("bank.dashboard"))
    acct.balance -= amount
    db.session.add(Tx(account_id=acct.id, kind="WITHDRAW", amount=amount, note="Prelievo"))
    db.session.commit()
    flash("Prelievo eseguito", "success")
    return redirect(url_for("bank.dashboard"))

@bp.post("/transfer")
def transfer():
    user = require_login()
    if not user:
        return redirect(url_for("auth.login"))
    target_username = (request.form.get("to") or "").strip()
    amount = parse_amount_to_cents(request.form.get("amount"))
    if amount <= 0:
        flash("Importo non valido", "error")
        return redirect(url_for("bank.dashboard"))
    target = User.query.filter_by(username=target_username).first()
    if not target or not target.account:
        flash("Destinatario inesistente", "error")
        return redirect(url_for("bank.dashboard"))
    src_acct = user.account
    dst_acct = target.account
    if amount > src_acct.balance:
        flash("Fondi insufficienti", "error")
        return redirect(url_for("bank.dashboard"))
    # Transazione semplice
    src_acct.balance -= amount
    dst_acct.balance += amount
    db.session.add(Tx(account_id=src_acct.id, kind="TRANSFER_OUT", amount=amount, note=f"-> {target.username}"))
    db.session.add(Tx(account_id=dst_acct.id, kind="TRANSFER_IN", amount=amount, note=f"<- {user.username}"))
    db.session.commit()
    flash("Bonifico eseguito", "success")
    return redirect(url_for("bank.dashboard"))
