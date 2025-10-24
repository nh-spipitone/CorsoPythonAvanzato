from datetime import datetime
from flask import current_app
from . import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey

# Gestiamo il denaro in centesimi (int) per evitare problemi di floating point
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    totp_secret: Mapped[str] = mapped_column(String(64), nullable=False)

    account = relationship("Account", back_populates="user", uselist=False)

class Account(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # denaro in centesimi
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="account")
    txs = relationship("Tx", back_populates="account", order_by="Tx.created_at.desc()")

class Tx(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)  # DEPOSIT, WITHDRAW, TRANSFER_OUT, TRANSFER_IN
    amount: Mapped[int] = mapped_column(Integer, nullable=False)   # centesimi
    note: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    account = relationship("Account", back_populates="txs")
