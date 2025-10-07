from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os, json

# crea app flask
app = Flask(__name__)
app.secret_key = "supersecretkey"

# file messaggi json
DATA_FILE = "data/messages.json"

# crea la cartella se non esiste
os.makedirs("data", exist_ok=True)


# funzione carica messaggi
def load_messages():

    # controlla se esistono messaggi
    if not os.path.exists(DATA_FILE):
        return []

    # apre e restituisce i contenuti del file json
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# funzione salva messaggi
def save_messages(messages):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


# home page con messaggi caricati
@app.route("/")
def home():
    page = int(request.args.get("page", 1))
    per_page = 10
    messages = load_messages()

    # odina i messaggi per id in modo decrescente
    messages = sorted(messages, key=lambda x: x["id"], reverse=True)

    total_pages = (len(messages) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_messages = messages[start:end]

    return render_template(
        "home.html", messages=page_messages, page=page, total_pages=total_pages
    )


# custom errore 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
