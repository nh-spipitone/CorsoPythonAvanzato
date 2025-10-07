# render_template mi serve per renderizzare file html, e flash utile per passare messaggi tramite la sessione di flask

import re
from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "testdev"
messagesList = ["Prova1", "Prova2"]

# Decorator che registra una route (percorso URL) nell'applicazione Flask.
# Quando un utente accede all'URL radice "/" (es. http://localhost:5000/),
# Flask invoca automaticamente la funzione sottostante (home).
# Il decorator collega il percorso HTTP alla funzione, creando un endpoint.
# Supporta metodi HTTP (GET di default) e può accettare parametri dinamici nell'URL.
# È il meccanismo fondamentale di routing di Flask per mappare URL a logica applicativa.


@app.get("/")
def home():
    # Passo la lista dei messaggi al template HTML tramite il parametro 'messages'
    return render_template("hellotest1.html", messages=messagesList[-20:])


@app.route("/new-message")
def show_message():
    # Restituisco una semplice stringa come risposta HTTP
    return render_template("form1.html")


@app.post("/new-author")
def add_author():
    author = (request.form.get("author") or "").strip()
    message = (request.form.get("message") or "").strip()
    if len(author) > 30:
        flash("Hai superato il limite di 30 caratteri")
        return redirect(url_for("show_message"))
    elif len(message) > 200:
        flash("Hai superato il limite di 200 caratteri")
        return redirect(url_for("show_message"))
    messagesList.append(f"{author}: {message}")
    return redirect(url_for("home"))
