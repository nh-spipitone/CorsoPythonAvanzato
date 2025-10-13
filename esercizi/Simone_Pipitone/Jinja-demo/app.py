
from flask import Flask, render_template
# TODO: aggiungi eventuali import (datetime, ecc.) se necessari

app = Flask(__name__)

# TODO: registra qui eventuali filtri custom, ad es. euro/dtit
# def euro(value): ...
# app.jinja_env.filters["euro"] = euro

@app.route("/")
def home():
    # TODO: passa una lista 'users' al template per il loop
    users = []  # es: [{"name":"...", "role":"...", "balance":0, "note_html":"...", "last_login": ...}, ...]
    return render_template("pages/home.html", users=users)

@app.route("/about")
def about():
    return render_template("pages/about.html")

if __name__ == "__main__":
    app.run(debug=True)
