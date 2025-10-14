"""
ESERCIZIO: BEARER TOKEN AUTHENTICATION CON WEB UI
==================================================
Implementa un sistema di autenticazione con Bearer Token usando:
- Login tramite form HTML
- Token salvato in session Flask
- Chiamate API protette usando il token dalla session

OBIETTIVI:
- Capire come integrare Bearer Token con una web app
- Gestire token lato client (session)
- Proteggere sia pagine web che endpoint API
"""

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    flash,
)
from functools import wraps
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

# =============================================================================
# TODO 1: Configura la SECRET_KEY per le sessioni Flask
# La secret key serve per firmare le sessioni in modo sicuro
# Usa secrets.token_hex(16) per generarla
# =============================================================================
app.config["SECRET_KEY"] = secrets.token_hex(16) # <-- IMPLEMENTA QUI


# =============================================================================
# CONFIGURAZIONE E DATI
# =============================================================================

# TODO 2: Crea un dizionario USERS con almeno 3 utenti di test
# Formato: {"username": "password"}
USERS = {"Mastella":"chofamiglia","Jimi_Hendrix":"voodoochild","Satana":"666"}  # <-- IMPLEMENTA QUI

# TODO 3: Crea dizionario ACTIVE_TOKENS per memorizzare i token
# Struttura: {token: {"username": str, "expires": datetime, "created": datetime}}
ACTIVE_TOKENS = {}  # <-- IMPLEMENTA QUI

# TODO 4: Definisci la durata del token (15 minuti)
TOKEN_EXPIRATION = timedelta(minutes=15)  # <-- IMPLEMENTA QUI


# =============================================================================
# FUNZIONI HELPER PER TOKEN
# =============================================================================


# TODO 5: Implementa generate_token()
# Genera un token sicuro usando secrets.token_urlsafe(32)
def generate_token():
    """Genera un token casuale sicuro."""
    return secrets.token_urlsafe(32) # <-- IMPLEMENTA QUI


# TODO 6: Implementa create_token(username)
# 1. Genera un nuovo token
# 2. Salvalo in ACTIVE_TOKENS con username, expires, created
# 3. Restituisci il token
def create_token(username):
    """Crea un nuovo token per l'utente."""
   
    new_token=generate_token()
    ACTIVE_TOKENS[new_token]={
        "username":username,
        "expires": datetime.now()+TOKEN_EXPIRATION,
        "created":datetime.now()
    }

    return new_token

    


# TODO 7: Implementa verify_token(token)
# 1. Verifica se esiste in ACTIVE_TOKENS
# 2. Controlla se è scaduto (datetime.now() > expires)
# 3. Se scaduto, rimuovilo
# 4. Restituisci username se valido, None altrimenti
def verify_token(token):
    """Verifica se un token è valido e non scaduto."""
    if token not in ACTIVE_TOKENS:
        return None
    token_data=ACTIVE_TOKENS[token]
    if token_data["expires"]<datetime.now():
        del ACTIVE_TOKENS[token]
        return None
    else: 
        return token_data["username"]
    
        
    


# =============================================================================
# DECORATOR PER PROTEZIONE WEB
# =============================================================================


# TODO 8: Implementa decorator login_required per le pagine web
# Questo decorator protegge le pagine HTML (non le API)
# 1. Controlla se 'token' esiste in session
# 2. Se non esiste, redirect a /login con messaggio flash
# 3. Se esiste, verifica validità con verify_token()
# 4. Se non valido, rimuovi da session e redirect a /login
# 5. Se valido, passa current_user alla funzione
def login_required(f):
    """Decorator per proteggere le pagine web."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = session["token"]

            
        if not token:
            flash("errore: È necessario fare login.")
            return redirect("login")
        username=verify_token(token)
        if not username:
            flash("È necessario necessario fare di nuovo login.")
            del session["token"]
            return redirect("login")
        # Passa l'username alla funzione
        return f(current_user=username, *args, **kwargs)

    return decorated


# TODO 9: Implementa decorator api_token_required per gli endpoint API
# Questo decorator protegge gli endpoint API (ritorna JSON)
# 1. Cerca token in session['token']
# 2. Se non c'è, restituisci JSON error 401
# 3. Verifica token con verify_token()
# 4. Se non valido, restituisci JSON error 401
# 5. Se valido, passa current_user alla funzione
def api_token_required(f):
    """Decorator per proteggere gli endpoint API."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = session["token"]
            
        if not token:
            return (jsonify(
                    {
                        "error":"Token non presente",
                        "message":"È necessario fare login per ottenere un token"
                    }
                ),
                401)
        username=verify_token(token)
        if not username:
            return (jsonify(
                    {
                        "error":"Token non valido o scaduto",
                        "message":"Verifica token fallita, necessario fare di nuovo login"
                    }
                ),
                401)
        # Passa l'username alla funzione
        return f(current_user=username, *args, **kwargs)

    return decorated


# =============================================================================
# ROUTE PUBBLICHE (WEB)
# =============================================================================


@app.route("/")
def home():
    """Homepage - mostra se l'utente è loggato o meno."""
    is_logged_in = "token" in session and verify_token(session["token"]) is not None
    current_user = None

    if is_logged_in:
        current_user = verify_token(session["token"])

    return render_template(
        "bearer_lab/index.html", is_logged_in=is_logged_in, current_user=current_user
    )


# TODO 10: Implementa route /login [GET, POST]
# GET: Mostra il form di login (template: bearer_lab/login.html)
# POST:
#   1. Ottieni username e password dal form
#   2. Valida contro USERS
#   3. Se valido: crea token, salvalo in session['token'], redirect a /dashboard
#   4. Se non valido: flash errore e mostra di nuovo il form
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login - form HTML."""
    if request.method=="POST":
        form=request.form
        username=form["username"]
        password=form["password"]
        if username in USERS.keys():
            if password in USERS.values():
                session['token']=create_token(username)
                return redirect("dashboard")
        flash("credenziali non valide")
    #arriva qui se il metodo è GET oppure se il POST non trova credenziali valide
    return render_template("bearer_lab/login.html")
    


# TODO 11: Implementa route /logout
# 1. Ottieni token da session
# 2. Se esiste, rimuovilo da ACTIVE_TOKENS
# 3. Rimuovi token dalla session
# 4. Flash messaggio di successo
# 5. Redirect a home
@app.route("/logout")
def logout():
    """Logout - invalida token e cancella session."""
    token=session['token']
    if token:
        del ACTIVE_TOKENS[token]
        flash("sei uscito")
    redirect("home")


# =============================================================================
# ROUTE PROTETTE (WEB)
# =============================================================================


# TODO 12: Implementa route /dashboard
# Usa @login_required
# Mostra template bearer_lab/dashboard.html con current_user
@app.route("/dashboard")
@login_required  # <-- DECOMMENTA
def dashboard(current_user=None):
    """Dashboard - area riservata."""
    return render_template("bearer_lab/login.html",current_user=current_user)


# TODO 13: Implementa route /profile
# Usa @login_required
# Mostra info utente e token (template: bearer_lab/token_info.html)
# Passa: username, created, expires, time_remaining
@app.route("/profile")
@login_required  # <-- DECOMMENTA
def profile(current_user=None):
    """Profilo utente - mostra info token."""
    token=session["token"]
    token_data=ACTIVE_TOKENS[token]
    username=token_data["username"]
    created=token_data["created"]
    expires=token_data["expires"]
    remaining=expires-datetime.now()
    return render_template("bearer_lab/token_info.html",username=username,created=created,expires=expires,remaining=remaining)


# =============================================================================
# ROUTE API (JSON) - Protette
# =============================================================================


# TODO 14: Implementa route /api/protected [GET]
# Usa @api_token_required
# Restituisci JSON con messaggio di benvenuto e current_user
@app.route("/api/protected")
@api_token_required  # <-- DECOMMENTA
def api_protected(current_user=None):
    """API protetta - richiede token valido."""
    return(jsonify(
        {
            "message":"Benvenuto "+ current_user
        }
    ))
    


# TODO 15: Implementa route /api/users [GET]
# Usa @api_token_required
# Restituisci JSON con lista di tutti gli username (NO password!)
@app.route("/api/users")
@api_token_required  # <-- DECOMMENTA
def api_users(current_user=None):
    """API - lista utenti."""
    return jsonify(USERS.keys())
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# ROUTE DEBUG
# =============================================================================


# TODO 16 (BONUS): Implementa route /admin/tokens
# Usa @login_required
# Mostra tutti i token attivi (template: bearer_lab/active_tokens.html)
# ATTENZIONE: Solo per debug, non usare in produzione!
@app.route("/admin/tokens")
# @login_required  # <-- DECOMMENTA
def admin_tokens(current_user=None):
    """Debug - mostra token attivi."""
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# ROUTE API PUBBLICA - Info Token
# =============================================================================


@app.route("/api/token/info")
def token_info():
    """API pubblica - info sul token corrente (se presente)."""
    if "token" not in session:
        return jsonify({"logged_in": False, "message": "Nessun token presente"})

    token = session["token"]
    username = verify_token(token)

    if not username:
        return jsonify({"logged_in": False, "message": "Token non valido o scaduto"})

    token_data = ACTIVE_TOKENS.get(token)
    if token_data:
        return jsonify(
            {
                "logged_in": True,
                "username": username,
                "token_created": token_data["created"].isoformat(),
                "token_expires": token_data["expires"].isoformat(),
                "time_remaining": str(token_data["expires"] - datetime.now()),
            }
        )

    return jsonify({"logged_in": False, "message": "Errore nel recupero dati token"})


# =============================================================================
# AVVIO APPLICAZIONE
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🔐 ESERCIZIO: BEARER TOKEN AUTHENTICATION CON WEB UI")
    print("=" * 70)
    print("\n📋 TODO da completare:")
    print("   1. Configurare SECRET_KEY")
    print("   2. Definire USERS, ACTIVE_TOKENS, TOKEN_EXPIRATION")
    print("   3. Implementare generate_token()")
    print("   4. Implementare create_token(username)")
    print("   5. Implementare verify_token(token)")
    print("   6. Implementare decorator login_required")
    print("   7. Implementare decorator api_token_required")
    print("   8. Implementare route /login")
    print("   9. Implementare route /logout")
    print("   10. Implementare route /dashboard")
    print("   11. Implementare route /profile")
    print("   12. Implementare route /api/protected")
    print("   13. Implementare route /api/users")
    print("   14. BONUS: Implementare route /admin/tokens")
    print("\n🌐 Una volta completato:")
    print("   1. Vai su http://localhost:5000")
    print("   2. Clicca su Login")
    print("   3. Usa le credenziali configurate in USERS")
    print("   4. Esplora Dashboard e Profile")
    print("   5. Prova le API con il browser o curl")
    print("\n📝 Credenziali suggerite:")
    print("   - admin / admin123")
    print("   - user / user456")
    print("   - test / test789")
    print("\n" + "=" * 70 + "\n")

    app.run(debug=True, port=5000)
