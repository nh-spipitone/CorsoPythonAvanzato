from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    flash,
    redirect,
    url_for
)
import secrets
from datetime import datetime
from token_service import verify_token, create_token,api_token_required, login_required, URL_TEMPLATES, USERS, ACTIVE_TOKENS, URL_ROUTES
from validators import LoginForm
from token_messages import protected_success

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(16)

# =============================================================================
# ROUTE PUBBLICHE (WEB)
# =============================================================================

@app.route("/")
def home():
    is_logged_in = "token" in session and verify_token(session["token"]) is not None
    current_user = None

    if is_logged_in:
        current_user = verify_token(session["token"])

    return render_template(
        URL_TEMPLATES.INDEX.value, is_logged_in=is_logged_in, current_user=current_user
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        form_data = LoginForm.model_validate(request.form)
        username = form_data.username
        password = form_data.password

        if username not in USERS or USERS.get(username) != password:
            flash("Credenziali non valide. Riprova.", "error")
            return render_template(URL_TEMPLATES.LOGIN.value)

        token = create_token(username)
        session["token"] = token
        
        flash(f"Benvenuto, {username}! Accesso effettuato.", "success")
        return redirect(url_for(URL_ROUTES.DASHBOARD.value))

    return render_template(URL_TEMPLATES.LOGIN.value)


@app.route("/logout")
def logout():
    token_to_delete = session.pop("token", None)

    if token_to_delete and token_to_delete in ACTIVE_TOKENS:
        del ACTIVE_TOKENS[token_to_delete]
        
    flash("Logout effettuato con successo. Arrivederci!", "success")
    return redirect(url_for(URL_ROUTES.LOGIN.value))


# =============================================================================
# ROUTE PROTETTE (WEB)
# =============================================================================

@app.route("/dashboard")
@login_required
def dashboard(current_user=None):
    return render_template(URL_TEMPLATES.DASHBOARD.value, current_user=current_user)


@app.route("/profile")
@login_required
def profile(current_user=None):

    token = session.get("token")
    token_data = ACTIVE_TOKENS.get(token, {})

    expires = token_data.get("expires")
    time_remaining = None
    if expires:
        remaining_time = expires - datetime.now()
        time_remaining = str(remaining_time).split(".")[0]
        if remaining_time.total_seconds() < 0:
            time_remaining = "Scaduto"

    return render_template(
    URL_TEMPLATES.PROFILE.value,
    current_user=current_user,
    created=token_data.get("created"),
    expires=expires,
    time_remaining=time_remaining
)

# =============================================================================
# ROUTE API (JSON) - Protette
# =============================================================================

@app.route("/api/protected")
@api_token_required
def api_protected(current_user=None):
    return protected_success(current_user)


@app.route("/api/users")
@api_token_required
def api_users(current_user=None):
    return jsonify({"users": list(USERS.keys())})

# =============================================================================
# ROUTE DEBUG
# =============================================================================

@app.route("/admin/tokens")
@login_required 
def admin_tokens(current_user=None):
    
    formatted_tokens = {}
    for token, data in ACTIVE_TOKENS.items():
        formatted_tokens[token] = {
            "username": data["username"],
            "created": data["created"].strftime("%Y-%m-%d %H:%M:%S"),
            "expires": data["expires"].strftime("%Y-%m-%d %H:%M:%S"),
        }

    return render_template(
        URL_TEMPLATES.ACTIVE_TOKENS.value,
        tokens=formatted_tokens,
        current_user=current_user,
    )

# =============================================================================
# ROUTE API PUBBLICA - Info Token
# =============================================================================


@app.route("/api/token/info")
def token_info():
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
