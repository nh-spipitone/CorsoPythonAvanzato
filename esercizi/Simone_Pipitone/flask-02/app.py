from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template_string,
    flash,
)  # Importa le classi e funzioni necessarie da Flask
from markupsafe import escape  # Importa escape per evitare injection di codice HTML

app = Flask(__name__)  # Crea un'applicazione Flask
app.secret_key = "dev"  # Imposta la chiave segreta necessaria per sessioni e flash

LOGIN_HTML = """
<!doctype html>
<title>Login</title>
<h1>Login</h1>
{% with msgs = get_flashed_messages() %}
    {% if msgs %}<p style="color:red">{{ msgs[0] }}</p>{% endif %}
{% endwith %}
<form method="post" action="{{ url_for('login') }}">
    <label>Username <input name="username"></label><br>
    <label>Password <input name="password" type="password"></label><br>
    <button type="submit">Entra</button>
</form>"""  # Template HTML per la pagina di login


@app.route("/welcome/<username>")  # Definisce la route /welcome/<username>
def welcome(username):  # Funzione associata alla route
    return f"Benvenuto, {escape(username)}!"  # Restituisce un messaggio di benvenuto, sanificando l'username


@app.route(
    "/login", methods=["GET", "POST"]
)  # Definisce la route /login per GET e POST
def login():  # Funzione associata alla route
    if request.method == "POST":  # Se la richiesta è POST
        username = request.form.get(
            "username", ""
        )  # Ottiene il valore di username dal form
        password = request.form.get(
            "password", ""
        )  # Ottiene il valore di password dal form
        if (
            username == "admin" and password == "secret"
        ):  # Controlla se le credenziali sono corrette
            return redirect(
                url_for("welcome", username=username)
            )  # Reindirizza alla pagina di benvenuto
        else:
            flash("Credenziali errate")  # Mostra un messaggio di errore
            return redirect(
                url_for("login")
            )  # Reindirizza nuovamente alla pagina di login
    return render_template_string(LOGIN_HTML)  # Se GET, mostra il form di login


# -------------------- alternativa --------------------
@app.get("/login")  # Definisce la route /login per richieste GET
def get_login():  # Funzione associata alla route GET /login
    return render_template_string(
        LOGIN_HTML
    )  # Mostra il form di login usando il template HTML


@app.post("/login")  # Definisce la route /login per richieste POST
def post_login():  # Funzione associata alla route POST /login
    username = request.form.get(
        "username", ""
    )  # Ottiene il valore di username dal form
    password = request.form.get(
        "password", ""
    )  # Ottiene il valore di password dal form
    if (
        username == "admin" and password == "secret"
    ):  # Controlla se le credenziali sono corrette
        return redirect(
            url_for("welcome", username=username)
        )  # Reindirizza alla pagina di benvenuto
    else:
        flash("Credenziali errate")  # Mostra un messaggio di errore
        return redirect(url_for("login"))  # Reindirizza nuovamente alla pagina di login


@app.route("/")  # Definisce la route principale /
def home():  # Funzione associata alla route
    link = url_for("login")  # Ottiene l'URL per la pagina di login
    return f'Vai a <a href="{link}">Login</a> per accedere al sistema.'  # Mostra un link per accedere al login
