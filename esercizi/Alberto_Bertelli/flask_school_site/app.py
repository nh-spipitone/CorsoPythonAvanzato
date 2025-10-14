from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, json
from json import JSONDecodeError
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.json")

app = Flask(__name__)

# --- Helpers ---
def load_db():
    """TODO: Leggi e ritorna il dict DB. Se non esiste, crealo con struttura vuota."""
    if not os.path.exists(DB_PATH):
        # TODO: crea file con struttura base e ritorna lo stesso dict
        db ={"students": [] , "grades":[],"attendance":[]}
        save_db(db)
        return db
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (JSONDecodeError, OSError):
        # TODO: gestisci file malformato (puoi rigenerarlo vuoto o mostrare errore)
        db ={"students": [] , "grades":[],"attendance":[]}
        save_db(db)
        return db

def save_db(db):
    with open(DB_PATH,"w",encoding="utf=8")as f:
            json.dump(db,f,indent=2)
            

def next_id(seq):
    """Ritorna il prossimo id intero per una lista di record con chiave 'id'."""
    return (max([r.get("id", 0) for r in seq]) + 1) if seq else 1

def get_student(db, student_id):
    """Ritorna lo studente per id, o None."""
    return next((s for s in db.get("students", []) if s.get("id") == student_id), None)

def compute_summary(db, student_id):
    """Calcola media voti e presenze per lo studente."""
    # TODO: completa
    
  

    voti =[v for v in db.get("grades",[]) if v.get("student_id") == student_id]
    attendance =[a for a in db.get("attendance",[]) if a.get("student_id") == student_id]
    mediaV=0
    presenze=0
    assente =0
    ritardo =0
    minuti =0
    
    for v in voti:
        mediaV +=v.get("value",0)
    mediaV= mediaV /len(voti)

    for a in attendance:
        if a.get("status") == "present":
            presenze +=1

        elif a.get("status") == "late":
            ritardo +=1
       
        elif a.get("status") == "absent":
            assente +=1





        
    return {
        "avg": mediaV,
        "count": len(voti),
        "present": presenze,
        "absent": assente,
        "late": ritardo,
        "minutes_late": 0,
    }

# --- Routes ---
@app.get("/")
def index():
    db = load_db()
    stats = {
        "total_students": len(db.get("students", [])),
        "total_grades": len(db.get("grades", [])),
        "total_attendance": len(db.get("attendance", [])),
    }
    return render_template("index.html", stats=stats)

@app.get("/students")
def students_list():
    db = load_db()
    return render_template("students.html", students=db.get("students", []))

@app.get("/students/<int:student_id>")
def student_detail(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    grades = [g for g in db.get("grades", []) if g.get("student_id") == student_id]
    attendance = [a for a in db.get("attendance", []) if a.get("student_id") == student_id]
    summary = compute_summary(db, student_id)
    return render_template("student_detail.html", student=student, grades=grades, attendance=attendance, summary=summary)

@app.get("/students/<int:student_id>/grade/new")
def new_grade(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    return render_template("form_grade.html", student=student, errors=[], form={"subject":"", "value":"", "date":""})

@app.post("/students/<int:student_id>/grade/new")
def create_grade(student_id):
    # TODO: valida e salva il voto nel DB
    # - subject (non vuoto)
    # - value float 0..10
    # - date YYYY-MM-DD
    # Redirect al dettaglio in caso di successo
    return ("TODO", 400)

@app.get("/students/<int:student_id>/attendance/new")
def new_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    return render_template("form_attendance.html", student=student, errors=[], form={"date":"", "status":"", "minutes_late":""})

@app.post("/students/<int:student_id>/attendance/new")
def create_attendance(student_id):
    # TODO: valida e salva la presenza nel DB
    # - date YYYY-MM-DD
    # - status in {present, absent, late}
    # - minutes_late richiesto se late
    return ("TODO", 400)

# --- API ---
@app.get("/api/students")
def api_students():
    db = load_db()
    return jsonify(db.get("students", []))

@app.get("/api/students/<int:student_id>")
def api_student(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return jsonify(error="not_found"), 404
    grades = [g for g in db.get("grades", []) if g.get("student_id") == student_id]
    attendance = [a for a in db.get("attendance", []) if a.get("student_id") == student_id]
    return jsonify({"student": student, "grades": grades, "attendance": attendance})

@app.post("/api/students/<int:student_id>/grades")
def api_create_grade(student_id):
    # TODO: valida body JSON e crea voto
    return jsonify(error="TODO"), 400

@app.post("/api/students/<int:student_id>/attendance")
def api_create_attendance(student_id):
    # TODO: valida body JSON e crea presenza
    return jsonify(error="TODO"), 400

if __name__ == "__main__":
    app.run(debug=True)
