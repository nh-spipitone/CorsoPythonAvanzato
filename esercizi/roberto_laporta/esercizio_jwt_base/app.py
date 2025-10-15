"""Mini esercizio: autenticazione JWT con Flask e note condivise."""

from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from flask import Flask, jsonify, request
import jwt

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-questa-chiave"

TOKEN_EXPIRATION = timedelta(minutes=45)
JWT_ALGORITHM = "HS256"

USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "password": "secret",
        "role": "admin",
        "email": "admin@example.com",
        "is_premium": True,
    },
    "writer": {
        "password": "penpassword",
        "role": "editor",
        "email": "writer@example.com",
        "is_premium": True,
    },
    "student": {
        "password": "learn123",
        "role": "user",
        "email": "student@example.com",
        "is_premium": False,
    },
}

NOTES: Dict[str, List[str]] = {username: [] for username in USERS}
JWT_ERRORS = (jwt.ExpiredSignatureError, jwt.InvalidTokenError)


def create_jwt(username: str) -> str:
    """TODO: costruisci e firma un JWT con claim personalizzati."""

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + TOKEN_EXPIRATION

    payload = { 
        "username": username,
        **USERS[username],
        "iat": issued_at,
        "exp": expires_at
    }

    token = jwt.encode(payload, app.config["SECRET_KEY"], JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    try:
        decoded = jwt.decode(token, app.config["SECRET_KEY"], JWT_ALGORITHM)
        return decoded
    except JWT_ERRORS:
        return None


def jwt_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decoratore base per proteggere le route con JWT."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        token = parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else None

        if not token:
            return (
                jsonify(
                    {
                        "error": "Token mancante",
                        "message": "Invia l'header Authorization: Bearer <token>",
                    }
                ),
                401,
            )

        payload = decode_jwt(token)
        if payload is None:
            return (
                jsonify(
                    {
                        "error": "Token non valido",
                        "message": "Effettua nuovamente il login per ottenere un token valido",
                    }
                ),
                401,
            )

        return func(current_user=payload, *args, **kwargs)

    return wrapper


def premium_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """TODO: permette l'accesso solo a utenti premium."""

    @wraps(func)
    @jwt_required
    def wrapper(current_user: Dict[str, Any], *args: Any, **kwargs: Any) -> Any:
        is_premium = current_user["is_premium"]
        if not is_premium:
            return jsonify({ "message": "Riservato a gli utenti premium"}), 403

        return func(current_user, *args, **kwargs)
    
    return wrapper


@app.get("/")
def home() -> Any:
    return jsonify(
        {
            "message": "Mini esercizio JWT",
            "info": "Completa login, token, decoratori e gestione note",
            "endpoints": {
                "POST /login": "Accetta credenziali e restituisce un token",
                "GET /protected": "Richiede token valido, restituisce messaggio personalizzato",
                "GET /me": "Mostra i claim presenti nel token",
                "POST /notes": "Salva una nota privata per l'utente loggato",
                "GET /notes/premium": "Disponibile solo per utenti premium, mostra tutte le note",
            },
        }
    )


@app.post("/login")
def login() -> Any:
    """TODO: valida credenziali, genera token e restituisci info utente."""
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return (
            jsonify(
                {
                    "error": "Dati mancanti",
                    "message": "Fornisci username e password nel body JSON",
                }
            ),
            400,
        )

    if username not in USERS or USERS[username]["password"] != password:
        return (
            jsonify(
                {
                    "error": "Credenziali non valide",
                    "message": "Controlla username e password",
                }
            ),
            401,
        )
    
    return create_jwt(username)


@app.get("/protected")
@jwt_required
def protected(current_user: Dict[str, Any]) -> Any:

    username = current_user["username"]

    return jsonify({
        "message": f"Benvenuto {username}, ecco il token"
    })



@app.get("/me")
@jwt_required
def me(current_user: Dict[str, Any]) -> Any:
    
    exp_claim = current_user["exp"]

    if isinstance(exp_claim, (int, float)):
        expires_at = datetime.fromtimestamp(exp_claim, tz=timezone.utc)
    else:
        expires_at = datetime.fromisoformat(str(exp_claim))

    remaining_time = max(int((expires_at - datetime.now(timezone.utc)).total_seconds()), 0)

    return jsonify({"message": f"Il tempo rimanente del token è {remaining_time}"})


@app.post("/notes")
@jwt_required
def add_note(current_user: Dict[str, Any]) -> Any:
    """TODO: salva una nota privata per l'utente corrente."""
    data = request.get_json(silent=True) or {}
    content = (data.get("text") or "").strip()
    username = current_user["username"]

    if not content:
        return (
            jsonify(
                {
                    "error": "Nota vuota",
                    "message": "Fornisci il campo text con contenuto non vuoto",
                }
            ),
            400,
        )

    notes = NOTES[username]
    notes.append(content)

    return jsonify({"notes": notes, "count": len(notes)})


@app.get("/notes/premium")
@premium_required
def premium_notes(current_user: Dict[str, Any]) -> Any:
    username = current_user["username"]
    notes = NOTES[username]

    return jsonify({"notes": notes, "count": len(notes)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
