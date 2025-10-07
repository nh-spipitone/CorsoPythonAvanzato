from flask import Flask, render_template, request, redirect

app = Flask(__name__)  # Crea un'istanza dell'app Flask


@app.get("/hello/<name>")  # Definisce la route /hello/<name>
@app.route("/hello")  # Definisce la route /hello/<name>
def hello(name=None):
    app.logger.debug(f"Hello {name}")  # Logga il nome ricevuto
    return render_template("hello.html", name=name)  # Mostra il template hello.html
