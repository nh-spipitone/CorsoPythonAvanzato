from flask import Flask, render_template
from datetime import datetime

# TODO: aggiungi eventuali import (datetime, ecc.) se necessari

app = Flask(__name__)


def euro(value) -> str:
    try:
        s = f"{float(value):,.2f} €"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(value)


def dtit(dt: datetime) -> str:
    if not isinstance(dt, datetime):
        print("dtit: valore non datetime:", dt)
        return str(dt)
    print("dtit:", dt)
    return dt.strftime("%d/%m/%Y %H:%M")


app.jinja_env.filters["euro"] = euro
app.jinja_env.filters["dtit"] = dtit


USERS = [
    {
        "name": "Mario Rossi",
        "role": "admin",
        "balance": 1000,
        "note_html": "<p>Note for Mario</p>",
        "last_login": datetime(2023, 1, 1, 12, 0),
    },
    {
        "name": "Anna Bianchi",
        "role": "guest",
        "balance": 0,
        "note_html": "<p>Note for Anna</p>",
        "last_login": datetime(2023, 2, 15, 14, 0),
    },
    {
        "name": "Luca Verdi",
        "role": "Moderator",
        "balance": 250.75,
        "note_html": "<p>Note for Luca</p>",
        "last_login": datetime(2023, 3, 10, 22, 30),
    },
    {
        "name": "Sara Neri",
        "role": "guest",
        "balance": 500.5,
        "note_html": "<p>Note for Sara</p>",
        "last_login": datetime(2023, 4, 5, 9, 15),
    },
]


@app.route("/")
def home():
    # TODO: passa una lista 'users' al template per il loop
    return render_template("pages/home.html", users=USERS)


@app.route("/about")
def about():
    return render_template("pages/about.html")


if __name__ == "__main__":
    app.run(debug=True)
