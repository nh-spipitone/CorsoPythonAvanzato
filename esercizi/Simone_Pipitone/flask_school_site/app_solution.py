from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, json
from json import JSONDecodeError
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.json")

app = Flask(__name__)

# --- Helpers ---
def empty_db():
    return {"students": [], "grades": [], "attendance": []}

def load_db():
    if not os.path.exists(DB_PATH):
        db = empty_db()
        save_db(db)
        return db
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Normalizza chiavi mancanti
            data.setdefault("students", [])
            data.setdefault("grades", [])
            data.setdefault("attendance", [])
            return data
    except (JSONDecodeError, OSError):
        # In caso di malformazione riparti da vuoto
        db = empty_db()
        save_db(db)
        return db

def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def next_id(seq):
    return (max([r.get("id", 0) for r in seq]) + 1) if seq else 1

def get_student(db, student_id):
    return next((s for s in db.get("students", []) if s.get("id") == student_id), None)

def parse_date_yyyy_mm_dd(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

def compute_summary(db, student_id):
    grades = [g for g in db.get("grades", []) if g.get("student_id") == student_id]
    attendance = [a for a in db.get("attendance", []) if a.get("student_id") == student_id]
    avg = sum(g.get("value", 0) for g in grades) / len(grades) if grades else 0.0
    present = sum(1 for a in attendance if a.get("status") == "present")
    absent = sum(1 for a in attendance if a.get("status") == "absent")
    late = sum(1 for a in attendance if a.get("status") == "late")
    minutes_late = sum(int(a.get("minutes_late") or 0) for a in attendance if a.get("status") == "late")
    return {"avg": avg, "count": len(grades), "present": present, "absent": absent, "late": late, "minutes_late": minutes_late}

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
    grades = sorted(grades, key=lambda g: (g.get("date") or "", g.get("id", 0)), reverse=True)
    attendance = [a for a in db.get("attendance", []) if a.get("student_id") == student_id]
    attendance = sorted(attendance, key=lambda a: (a.get("date") or "", a.get("id", 0)), reverse=True)
    summary = compute_summary(db, student_id)
    return render_template("student_detail.html", student=student, grades=grades, attendance=attendance, summary=summary)

@app.get("/students/<int:student_id>/grade/new")
def new_grade(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("form_grade.html", student=student, errors=[], form={"subject":"", "value":"", "date": today})

@app.post("/students/<int:student_id>/grade/new")
def create_grade(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)

    subject = (request.form.get("subject") or "").strip()
    value_raw = (request.form.get("value") or "").strip()
    date_s = (request.form.get("date") or "").strip()

    errors = []
    if not subject:
        errors.append("La materia è obbligatoria.")
    try:
        value = float(value_raw)
        if not (0 <= value <= 10):
            errors.append("Il voto deve essere tra 0 e 10.")
    except ValueError:
        errors.append("Il voto deve essere numerico.")
        value = None

    if not parse_date_yyyy_mm_dd(date_s):
        errors.append("Data non valida. Usa formato YYYY-MM-DD.")

    if errors:
        return render_template("form_grade.html", student=student, errors=errors, form={"subject": subject, "value": value_raw, "date": date_s}), 400

    grade = {"id": next_id(db["grades"]), "student_id": student_id, "subject": subject, "value": value, "date": date_s}
    db["grades"].append(grade)
    save_db(db)
    return redirect(url_for("student_detail", student_id=student_id))

@app.get("/students/<int:student_id>/attendance/new")
def new_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("form_attendance.html", student=student, errors=[], form={"date": today, "status": "", "minutes_late": ""})

@app.post("/students/<int:student_id>/attendance/new")
def create_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)

    date_s = (request.form.get("date") or "").strip()
    status = (request.form.get("status") or "").strip()
    minutes_raw = (request.form.get("minutes_late") or "").strip()

    errors = []
    if not parse_date_yyyy_mm_dd(date_s):
        errors.append("Data non valida. Usa formato YYYY-MM-DD.")
    if status not in {"present", "absent", "late"}:
        errors.append("Stato non valido (present/absent/late).")
    minutes = 0
    if status == "late":
        if minutes_raw == "":
            errors.append("Minuti di ritardo richiesti per status 'late'.")
        else:
            try:
                minutes = int(minutes_raw)
                if minutes < 0:
                    errors.append("Minuti di ritardo deve essere >= 0.")
            except ValueError:
                errors.append("Minuti di ritardo deve essere un intero.")

    if errors:
        return render_template("form_attendance.html", student=student, errors=errors, form={"date": date_s, "status": status, "minutes_late": minutes_raw}), 400

    att = {"id": next_id(db["attendance"]), "student_id": student_id, "date": date_s, "status": status, "minutes_late": minutes if status == "late" else 0}
    db["attendance"].append(att)
    save_db(db)
    return redirect(url_for("student_detail", student_id=student_id))

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
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return jsonify(error="not_found"), 404
    if not request.is_json:
        return jsonify(error="json_required"), 400
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    value = data.get("value")
    date_s = (data.get("date") or "").strip()
    if not subject or not isinstance(value, (int, float)) or not (0 <= float(value) <= 10) or not parse_date_yyyy_mm_dd(date_s):
        return jsonify(error="invalid_payload"), 400
    grade = {"id": next_id(db["grades"]), "student_id": student_id, "subject": subject, "value": float(value), "date": date_s}
    db["grades"].append(grade)
    save_db(db)
    return jsonify(grade), 201

@app.post("/api/students/<int:student_id>/attendance")
def api_create_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return jsonify(error="not_found"), 404
    if not request.is_json:
        return jsonify(error="json_required"), 400
    data = request.get_json(silent=True) or {}
    date_s = (data.get("date") or "").strip()
    status = (data.get("status") or "").strip()
    minutes = int(data.get("minutes_late") or 0)
    if not parse_date_yyyy_mm_dd(date_s) or status not in {"present", "absent", "late"}:
        return jsonify(error="invalid_payload"), 400
    if status == "late" and minutes < 0:
        return jsonify(error="invalid_minutes"), 400
    att = {"id": next_id(db["attendance"]), "student_id": student_id, "date": date_s, "status": status, "minutes_late": minutes if status == "late" else 0}
    db["attendance"].append(att)
    save_db(db)
    return jsonify(att), 201

if __name__ == "__main__":
    app.run(debug=True)
