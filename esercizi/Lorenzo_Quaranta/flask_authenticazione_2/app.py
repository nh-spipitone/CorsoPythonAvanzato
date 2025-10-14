from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here-change-in-production"

# Inizializza Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = (
    "Per favore effettua il login per accedere a questa pagina."
)

# Database simulato (in produzione usare un vero database)
users_db = {
    "admin": {"password": generate_password_hash("admin123"), "name": "Amministratore"},
    "user": {"password": generate_password_hash("user123"), "name": "Utente Demo"},
}


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.name = users_db[username]["name"]


@login_manager.user_loader
def load_user(username):
    if username in users_db:
        return User(username)
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember", False))
        if username in users_db and check_password_hash(
            users_db[username]["password"], password
        ):
            user = User(username)
            login_user(user, remember=remember)
            flash("Login effettuato con successo!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        else:
            flash("Credenziali non valide. Riprova.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        name = request.form.get("name", "")

        if username in users_db:
            flash("Username già esistente. Scegli un altro.", "danger")
        else:
            users_db[username] = {
                "password": generate_password_hash(password),
                "name": name,
            }
            flash("Registrazione avvenuta con successo! Effettua il login.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.name)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)
