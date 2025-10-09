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


# nuovo messaggio
@app.route("/new", methods=["GET"])
def new_message():
    return render_template("new.html")


# invio form nuvo messaggio
@app.route("/new", methods=["POST"])
def post_message():
    author = request.form.get("author", "").strip()
    text = request.form.get("text", "").strip()

    # controlli
    errors = []
    if not author:
        errors.append("Author cannot be empty.")
    elif len(author) > 30:
        errors.append("Author max 30 chars.")
    if not text:
        errors.append("Message cannot be empty.")
    elif len(text) > 200:
        errors.append("Message max 200 chars.")

    if errors:
        for e in errors:
            flash(e, "error")
        return render_template("new.html", author=author, text=text), 400

    messages = load_messages()
    next_id = max([m["id"] for m in messages], default=0) + 1
    messages.append({"id": next_id, "author": author, "text": text})
    save_messages(messages)

    flash("Message posted!", "success")
    return redirect(url_for("home"))


# mostra singolo messaggio
@app.route("/msg/<int:msg_id>")
def show_message(msg_id):
    messages = load_messages()
    msg = next((m for m in messages if m["id"] == msg_id), None)
    if not msg:
        return render_template("404.html"), 404
    return render_template("show.html", message=msg)


# custom errore 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
