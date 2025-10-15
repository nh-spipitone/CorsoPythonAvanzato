from flask import jsonify

def malformed_error():
    return (
        jsonify(
            {
                "error": "Token malformato",
                "message": "Richiesto formato: [Authorization: Bearer <token>]"
            }
        ),
        401
    )                

def missing_token():
    return (
        jsonify(
            {
                "error": "Token mancante",
                "message": "Effettua il login per ottenere un token",
            }
        ),
        401,
    )

def expired_token():
    return (
        jsonify(
            {
                "error": "Token non valido o scaduto",
                "message": "Effettua nuovamente il login",
            }
        ),
        401,
    )

def wrong_credentials():
    return (
        jsonify(
            {
                "error": "Credenziali non valide",
                "message": "Username o password errati",
            }
        ),
        401,
    )

def login_success(token: str, expiration):
    return (
        jsonify(
            {
                "message": "Login effettuato con successo",
                "token": token,
                "token_type": "Bearer",
                "expires_in": int(expiration.total_seconds()),
                "usage": f"Authorization: Bearer {token}",
            }
        ),
        200,
    )

def protected_success(current_user):
    return jsonify(
        {
            "message": f"Accesso API protetta riuscito. Benvenuto, {current_user}!",
            "user": current_user,
        }
    )