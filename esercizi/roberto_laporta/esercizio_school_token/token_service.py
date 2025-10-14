from enum import Enum
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, session, flash, redirect, url_for
from token_messages import malformed_error, missing_token, expired_token

USERS = {
    "admin": "admin123",
    "user": "user456",
    "test": "test789"
}

class URL_ROUTES(Enum):
    DASHBOARD = "dashboard"
    LOGIN = "login"
    INDEX = "index"

class URL_TEMPLATES(Enum):
    INDEX = "index.html"
    LOGIN = "login.html"
    DASHBOARD = "dashboard.html"
    PROFILE = "token_info.html"

ACTIVE_TOKENS = {}

TOKEN_EXPIRATION = timedelta(minutes=15)

def generate_token():
    token = secrets.token_urlsafe(32)
    return token

def create_token(username: str):
    token = generate_token()
    ACTIVE_TOKENS[token] = {
        "username": username,
        "expires": datetime.now() + TOKEN_EXPIRATION,
        "created": datetime.now()
    }

    return token

def verify_token(token):
    if token not in ACTIVE_TOKENS:
        return None

    token_data = ACTIVE_TOKENS[token]

    if datetime.now() > token_data["expires"]:
        del ACTIVE_TOKENS[token]
        return None
    
    return token_data["username"]

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if "token" not in session:
            flash("Effettuare il login per accedere", "error")
            return redirect(url_for(URL_ROUTES.LOGIN.value))
        
        username = verify_token(session.get("token"))
        if not username:
            session.pop("token", None)
            flash("Il token della sessione è scaduto", "error")
            return expired_token()

        return f(current_user=username, *args, **kwargs)

    return decorated

def api_token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return malformed_error()
        
            if not token:
                return missing_token()
                
            username = verify_token(token)
            if not username:
                return expired_token()
            
            return f(current_user=username, *args, **kwargs)
        
    return decorated
