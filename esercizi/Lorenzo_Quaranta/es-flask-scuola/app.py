'''
Realizza una mini web‑app Flask che emula un sito scolastico con:

elenco studenti,
dettaglio studente con media voti e presenze/assenze/ritardi,
moduli per inserire nuovi voti e nuove presenze,
salvataggio su file JSON (db.json), senza database esterni.
'''
from flask import Flask, render_template, request, redirect,url_for,flash
import json, os, datetime

app = Flask(__name__)
#init e controllo esistenza file json
default_json_structure={ "students": [], "grades": [], "attendance": [] }

if( not os.path.exists("db.json")):
       with open("db.json","x",encoding="utf-8") as db_json:
              json.dump(default_json_structure,db_json,indent=2, ensure_ascii=False)

def load_db():
      with open("db.json", "r", encoding="utf-8") as db_file:
             return json.load(db_file)

def save_db():
      pass

def next_id(seq):
      return(seq[-1]["id"]+1) if seq else 1

def get_student(db, id):
      pass

@app.route("/")
def show_dashboard():
        pass

@app.route("/students")
def get_students():
        pass

@app.route("/students/<int:student_id>")
def show_single_student(student_id):
        pass

@app.route("/students/<id>/grade/new",methods=["GET","POST"])
def new_grade(id):
        pass

@app.route("/students/<id>/attendance/new",methods=["GET","POST"])
def attendance(id):
        pass

@app.route("/api/students")
def load_students():
        return load_db()["students"]

@app.route("/api/students/<id>")
def get_single_student(id):
        pass

@app.route("/api/students/<id>/grades",methods=["POST"])
def upload_student_grade(id):
        pass

@app.route("/api/students/<id>/attendance",methods=["POST"])
def upload_student_attendance(id):
        pass
if __name__=="__main__":
    app.run(debug=True)