"""
JWT (JSON WEB TOKEN) AUTHENTICATION
====================================
Autenticazione con JWT - token firmati che contengono informazioni (payload).
I JWT sono self-contained: il server può verificarli senza database lookup.

Struttura JWT: header.payload.signature
- Header: tipo token e algoritmo
- Payload: dati utente (claims)
- Signature: firma per verificare autenticità

RICHIEDE: pip install pyjwt
"""

from flask import Flask, request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# SECRET KEY per firmare i JWT (in produzione: usa variabile d'ambiente!)
app.config["SECRET_KEY"] = "super-secret-jwt-key-change-in-production"

# Database simulato
USERS = {
    "admin": {"password": "secret", "role": "admin", "email": "admin@example.com"},
    "user": {"password": "password123", "role": "user", "email": "user@example.com"},
}

# Durata del token
TOKEN_EXPIRATION = timedelta(hours=1)


def create_jwt(username):
    """Crea un JWT per l'utente."""
    user_data = USERS[username]

    # Payload del token (claims)
    payload = {
        "username": username,
        "role": user_data["role"],
        "email": user_data["email"],
        "iat": datetime.now(timezone.utc),  # Issued At
        "exp": datetime.now(timezone.utc) + TOKEN_EXPIRATION,  # Expiration
    }

    # Crea e firma il JWT
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

    return token


def verify_jwt(token):
    """Verifica e decodifica un JWT."""
    try:
        # Decodifica e verifica il token
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token scaduto
    except jwt.InvalidTokenError:
        return None  # Token non valido


def jwt_required(f):
    """Decorator per proteggere le route con JWT."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Cerca il token nell'header Authorization
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
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
                        "message": "Effettua il login per ottenere un JWT",
                    }
                ),
                401,
            )

        # Verifica il JWT
        payload = verify_jwt(token)
        if not payload:
            return (
                jsonify(
                    {
                        "error": "Token non valido o scaduto",
                        "message": "Effettua nuovamente il login",
                    }
                ),
                401,
            )

        # Passa i dati del token alla funzione
        return f(current_user=payload, *args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator per route che richiedono ruolo admin."""

    @wraps(f)
    @jwt_required
    def decorated(current_user, *args, **kwargs):
        if current_user.get("role") != "admin":
            return (
                jsonify(
                    {
                        "error": "Accesso negato",
                        "message": "Solo gli amministratori possono accedere a questa risorsa",
                    }
                ),
                403,
            )

        return f(current_user=current_user, *args, **kwargs)

    return decorated


@app.route("/")
def home():
    """Route pubblica."""
    return jsonify(
        {
            "message": "JWT Authentication Demo",
            "info": "JSON Web Token con expiration e role-based access",
            "endpoints": {
                "POST /login": "Ottieni un JWT (username + password)",
                "GET /protected": "Risorsa protetta (richiede JWT)",
                "GET /me": "Info utente dal JWT",
                "GET /admin": "Risorsa admin (richiede ruolo admin)",
                "POST /refresh": "Rinnova il JWT",
            },
        }
    )


@app.route("/login", methods=["POST"])
def login():
    """Endpoint di login - restituisce un JWT."""
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
    if username not in USERS or USERS[username]["password"] != password:
        return jsonify({"error": "Credenziali non valide"}), 401

    # Genera JWT
    token = create_jwt(username)

    return (
        jsonify(
            {
                "message": "Login effettuato con successo",
                "token": token,
                "token_type": "Bearer",
                "expires_in": int(TOKEN_EXPIRATION.total_seconds()),
                "user": {
                    "username": username,
                    "role": USERS[username]["role"],
                    "email": USERS[username]["email"],
                },
            }
        ),
        200,
    )


@app.route("/protected")
@jwt_required
def protected(current_user):
    """Route protetta - richiede JWT valido."""
    return jsonify(
        {
            "message": f"Benvenuto {current_user['username']}!",
            "user_info": current_user,
            "data": "Dati protetti accessibili con JWT valido",
        }
    )


@app.route("/me")
@jwt_required
def me(current_user):
    """Restituisce info sull'utente dal JWT (senza database lookup!)."""
    # Calcola tempo rimanente
    exp_timestamp = current_user["exp"]
    expires_at = datetime.fromtimestamp(exp_timestamp)
    time_remaining = expires_at - datetime.now()

    return jsonify(
        {
            "username": current_user["username"],
            "email": current_user["email"],
            "role": current_user["role"],
            "token_issued_at": datetime.fromtimestamp(current_user["iat"]).isoformat(),
            "token_expires_at": expires_at.isoformat(),
            "time_remaining_seconds": int(time_remaining.total_seconds()),
        }
    )


@app.route("/admin")
@admin_required
def admin(current_user):
    """Route admin - richiede JWT con ruolo admin."""
    return jsonify(
        {
            "message": f"Benvenuto Admin {current_user['username']}!",
            "admin_data": "Questi dati sono accessibili solo agli admin",
            "all_users": list(USERS.keys()),
        }
    )


@app.route("/refresh", methods=["POST"])
@jwt_required
def refresh(current_user):
    """Rinnova il JWT (genera un nuovo token)."""
    new_token = create_jwt(current_user["username"])

    return jsonify(
        {
            "message": "Token rinnovato con successo",
            "token": new_token,
            "token_type": "Bearer",
            "expires_in": int(TOKEN_EXPIRATION.total_seconds()),
        }
    )


@app.route("/decode-jwt", methods=["POST"])
def decode_jwt():
    """Debug: decodifica un JWT senza verificarlo (solo per demo!)."""
    data = request.get_json()

    if not data or "token" not in data:
        return jsonify({"error": "Fornisci un token"}), 400

    try:
        # Decodifica SENZA verifica (solo per vedere il contenuto)
        payload = jwt.decode(data["token"], options={"verify_signature": False})
        return jsonify(
            {
                "message": "JWT decodificato (non verificato!)",
                "header": jwt.get_unverified_header(data["token"]),
                "payload": payload,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔐 JWT AUTHENTICATION DEMO")
    print("=" * 60)
    print("\nServer in esecuzione su http://localhost:5000")
    print("\n⚠️  IMPORTANTE: Installa PyJWT con: pip install pyjwt")
    print("\n📝 Credenziali di test:")
    print("   - Admin: username=admin, password=secret")
    print("   - User: username=user, password=password123")
    print("\n🧪 Comandi di test:")
    print("\n   # 1. Login per ottenere un JWT:")
    print(
        '   curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\\"username\\":\\"admin\\",\\"password\\":\\"secret\\"}"'
    )
    print("\n   # 2. Usare il JWT (sostituisci YOUR_JWT):")
    print('   curl http://localhost:5000/protected -H "Authorization: Bearer YOUR_JWT"')
    print("\n   # 3. Info utente dal JWT:")
    print('   curl http://localhost:5000/me -H "Authorization: Bearer YOUR_JWT"')
    print("\n   # 4. Accesso admin:")
    print('   curl http://localhost:5000/admin -H "Authorization: Bearer YOUR_JWT"')
    print("\n   # 5. Rinnova token:")
    print(
        '   curl -X POST http://localhost:5000/refresh -H "Authorization: Bearer YOUR_JWT"'
    )
    print("\n" + "=" * 60 + "\n")

    app.run(debug=True, port=5000)
