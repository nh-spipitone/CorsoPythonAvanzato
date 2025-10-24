from flask import Flask, render_template, request, redirect,url_for,flash,session
import sqlite3, os, time
from werkzeug.security import (
generate_password_hash,
check_password_hash,
)

import pyotp

app = Flask(__name__)
app.config["SECRET_KEY"]="change-me"

DB_PATH = os.path.join(os.path.dirname(__file__), "app_db.db")



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            secret_key TEXT NOT NULL
        );
        """)

with app.app_context():
    init_db()
    with get_db() as db:
        #TODO:hashing password
        password="napoli1"
        secretkey="cambiami"
        db.execute("INSERT OR IGNORE INTO users (username,password,secret_key) VALUES (?,?,?)",
                   ("mario",password,secretkey))


@app.get("/")
def index():
    if session.get("userid"):
        return render_template("index.html")
    else: 
        return redirect(url_for("login"))

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def auth():
    user=request.form["username"]
    password=request.form["password"]
    print(user)
    #TODO:hashing password
    with get_db() as db:
        row=db.execute("SELECT id,username,password FROM USERS WHERE username=?",(user,)).fetchone()
        if row:
            retrieved_password=row["password"]
            user_id=row['id']
            if password==retrieved_password:
                session['pending_userid']=user_id
                return redirect(url_for("otp"))
        flash("credenziali non valide","error")
        return redirect(url_for('login'))
    
@app.get("/otp")
def otp():
    if session["pending_userid"]:
        return render_template("otp.html")
    else:
        return redirect(url_for('login'))

@app.post("/otp")
def otp_post():
    if session["pending_userid"]:
        code=request.form["code"]
        user_id=str(session["pending_userid"])
        with get_db() as db:
            row=db.execute("SELECT secret_key FROM USERS WHERE id=?",(user_id)).fetchone()
            if row:
                key=row["secret_key"]
                totp = pyotp.TOTP(key)
                if not code or not totp.verify(code, valid_window=1):
                    flash("OTP non valido o scaduto", "error")
                    return redirect(url_for("otp"))
                else: 
                    flash("autenticazione riuscita","success")
                    session["userid"]=session["pending_userid"]
                    session.pop("pending_userid",None)
                    return redirect(url_for("index"))

                
    else:
        flash("autenticazione fallita","error")
        return redirect(url_for('login'))

    
if __name__=="__main__":
    app.run(debug=True)
        


