# app.py  # Nome del file

from flask import (
    Flask,
    url_for,
)  # Importa la classe Flask e la funzione url_for dal modulo flask
from markupsafe import (
    escape,
)  # Importa la funzione escape per evitare injection di codice

app = Flask(__name__)  # Crea un'istanza dell'app Flask


@app.route("/")  # Definisce la route per la homepage "/"
def home():  # Funzione associata alla route "/"
    link = url_for(
        "hello", name="Simone"
    )  # Genera l'URL per la route 'hello' passando il parametro 'name'
    return f'vai a <a href="{link}">{link}</a>'  # Restituisce un link HTML alla pagina hello


@app.route("/hello/<name>")  # Definisce la route con parametro 'name'
def hello(name):  # Funzione associata alla route "/hello/<name>"
    return (
        f"Ciao, {escape(name)}!"  # Restituisce un saluto, usando escape per sicurezza
    )


@app.route("/boom")  # Definisce la route "/boom"
def boom():  # Funzione associata alla route "/boom"
    return 1 / 0  # Restituisce la 1 / 0  darà un errore  che non supporta un float


# if __name__ == "__main__":      # Controlla se il file è eseguito direttamente
#     app.run(debug=True)         # Avvia il server Flask in modalità debug (commentato)
# comando da terminale per eseguire l'app: flask --app esercizi/Simone_Pipitone/flask-01/app.py run --debug
