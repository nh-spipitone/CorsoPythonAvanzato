"""
BEARER TOKEN AUTHENTICATION
============================
Autenticazione tramite token Bearer nell'header Authorization.
L'utente fa login e riceve un token da usare per le richieste successive.

Format: Authorization: Bearer <token>
"""

from flask import Flask, request, jsonify
from functools import wraps
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

# Database simulato
USERS = {"admin": "secret", "user": "password123"}

# Storage dei token attivi (in produzione: usa Redis o database)
# Struttura: {token: {"username": str, "expires": datetime}}
ACTIVE_TOKENS = {}

# Durata del token (30 minuti)
TOKEN_EXPIRATION = timedelta(minutes=30)


def generate_token():
    """Genera un token casuale sicuro."""
    return secrets.token_urlsafe(32)


def create_token(username):
    """Crea un nuovo token per l'utente."""
    token = generate_token()
    ACTIVE_TOKENS[token] = {
        "username": username,
        "expires": datetime.now() + TOKEN_EXPIRATION,
        "created": datetime.now(),
    }
    return token


def verify_token(token):
    """Verifica se un token è valido e non scaduto."""
    if token not in ACTIVE_TOKENS:
        return None

    token_data = ACTIVE_TOKENS[token]

    # Verifica scadenza
    if datetime.now() > token_data["expires"]:
        # Token scaduto, rimuovilo
        del ACTIVE_TOKENS[token]
        return None

    return token_data["username"]


def token_required(f):
    """Decorator per proteggere le route con Bearer Token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Cerca il token nell'header Authorization
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return (
                    jsonify(
                        {
                            "error": "Token malformato",
                            "message": "Usa il formato: Authorization: Bearer <token>",
                        }
                    ),
                    401,
                )

        if not token:
            return (
                jsonify(
                    {
                        "error": "Token mancante",
                        "message": "Effettua il login per ottenere un token",
                    }
                ),
                401,
            )

        # Verifica il token
        username = verify_token(token)
        if not username:
            return (
                jsonify(
                    {
                        "error": "Token non valido o scaduto",
                        "message": "Effettua nuovamente il login",
                    }
                ),
                401,
            )

        # Passa l'username alla funzione
        return f(current_user=username, *args, **kwargs)

    return decorated


@app.route("/")
def home():
    """Route pubblica."""
    return jsonify(
        {
            "message": "Bearer Token Authentication Demo",
            "endpoints": {
                "POST /login": "Ottieni un token (username + password)",
                "GET /protected": "Risorsa protetta (richiede token)",
                "GET /me": "Info utente corrente (richiede token)",
                "POST /logout": "Invalida il token corrente",
            },
        }
    )


@app.route("/login", methods=["POST"])
def login():
    """Endpoint di login - restituisce un token."""
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return (
            jsonify(
                {"error": "Dati mancanti", "message": "Fornisci username e password"}
            ),
            400,
        )

    username = data["username"]
    password = data["password"]

    # Verifica credenziali
    if username not in USERS or USERS[username] != password:
        return (
            jsonify(
                {
                    "error": "Credenziali non valide",
                    "message": "Username o password errati",
                }
            ),
            401,
        )

    # Genera token
    token = create_token(username)

    return (
        jsonify(
            {
                "message": "Login effettuato con successo",
                "token": token,
                "token_type": "Bearer",
                "expires_in": int(TOKEN_EXPIRATION.total_seconds()),
                "usage": f"Authorization: Bearer {token}",
            }
        ),
        200,
    )


@app.route("/protected")
@token_required
def protected(current_user):
    """Route protetta - richiede token valido."""
    return jsonify(
        {
            "message": f"Benvenuto {current_user}!",
            "user": current_user,
            "data": "Questi sono dati protetti accessibili solo con un token valido",
        }
    )


@app.route("/me")
@token_required
def me(current_user):
    """Restituisce info sull'utente corrente."""
    # Trova il token dall'header
    token = request.headers["Authorization"].split(" ")[1]
    token_data = ACTIVE_TOKENS[token]

    return jsonify(
        {
            "username": current_user,
            "token_created": token_data["created"].isoformat(),
            "token_expires": token_data["expires"].isoformat(),
            "time_remaining": str(token_data["expires"] - datetime.now()),
        }
    )


@app.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    """Logout - invalida il token corrente."""
    token = request.headers["Authorization"].split(" ")[1]

    if token in ACTIVE_TOKENS:
        del ACTIVE_TOKENS[token]

    return jsonify({"message": "Logout effettuato con successo", "user": current_user})


@app.route("/tokens/active")
def active_tokens():
    """Debug: mostra i token attivi (NON usare in produzione!)."""
    tokens_info = []
    for token, data in ACTIVE_TOKENS.items():
        tokens_info.append(
            {
                "token": token[:10] + "...",  # Mostra solo i primi 10 caratteri
                "username": data["username"],
                "expires": data["expires"].isoformat(),
                "is_expired": datetime.now() > data["expires"],
            }
        )

    return jsonify({"active_tokens_count": len(ACTIVE_TOKENS), "tokens": tokens_info})


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔐 BEARER TOKEN AUTHENTICATION DEMO")
    print("=" * 60)
    print("\nServer in esecuzione su http://localhost:5000")
    print("\n📝 Credenziali di test:")
    print("   - Username: admin, Password: secret")
    print("   - Username: user, Password: password123")
    print("\n🧪 Comandi di test:")
    print("\n   # 1. Login per ottenere un token:")
    print(
        '   curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\\"username\\":\\"admin\\",\\"password\\":\\"secret\\"}"'
    )
    print("\n   # 2. Usare il token ricevuto (sostituisci YOUR_TOKEN):")
    print(
        '   curl http://localhost:5000/protected -H "Authorization: Bearer YOUR_TOKEN"'
    )
    print("\n   # 3. Info utente corrente:")
    print('   curl http://localhost:5000/me -H "Authorization: Bearer YOUR_TOKEN"')
    print("\n   # 4. Logout:")
    print(
        '   curl -X POST http://localhost:5000/logout -H "Authorization: Bearer YOUR_TOKEN"'
    )
    print("\n   # 5. Vedere token attivi (debug):")
    print("   curl http://localhost:5000/tokens/active")
    print("\n" + "=" * 60 + "\n")

    app.run(debug=True, port=5000)
