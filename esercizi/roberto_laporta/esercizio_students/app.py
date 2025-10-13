from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from helpers import load_db, get_student, compute_summary, next_id, save_db, statusEnum

app = Flask(__name__)

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
    db = load_db()
    student = get_student(db,student_id)

    if student is None:
        return ("Errore: Studente non trovato.", 400)

    subject = request.form.get("subject")
    raw_value = request.form.get("value")
    date = request.form.get("date")

    if not subject or raw_value is None or not date:
        return ("Errore: I campi 'subject', 'value' e 'date' sono obbligatori.", 400)

    try:
        value = float(raw_value)
    except (ValueError):
        return ("Errore: Il voto 'value' deve essere un numero valido.", 400)

    if not (0.0 <= value <= 10.0):
        return ("Errore: Il voto 'value' deve essere compreso tra 0 e 10.", 400)
    
    grades = db.get("grades", [])

    new_grade = {
        "id": next_id(grades),
        "student_id": student_id,
        "subject": subject.strip(),
        "value": value,
        "date": date
    }

    db["grades"].append(new_grade)
    save_db(db)

    return redirect(url_for('student_detail', student_id=student_id))

@app.get("/students/<int:student_id>/attendance/new")
def new_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    return render_template("form_attendance.html", student=student, errors=[], form={"date":"", "status":"", "minutes_late":""})

@app.post("/students/<int:student_id>/attendance/new")
def create_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)

    if not student:
        return ("Studente non trovato", 404)
    
    attendances = db.get("attendance", [])
    date = request.form.get("date")
    status = request.form.get("status")
    minutes_late = request.form.get("minutes_late")

    new_attendance = {
        "id": next_id(attendances),
        "student_id": student_id,
        "date": date,
        "status": status,
    }

    if not status or not date:
        return ("Errore: I campi 'date' e 'status'sono obbligatori.", 400)

    if status == statusEnum.LATE.value:
        if not minutes_late:
            return ("Errore: È obbligatorio specificate i minuti di ritardo", 400)
        else:
            new_attendance["minutes_late"] = int(minutes_late)
        
    db["attendance"].append(new_attendance)
    save_db(db)

    return redirect(url_for('student_detail', student_id=student_id))

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

    required_fields = ["subject", "value", "date"]

    if not student:
        return jsonify("Studente non trovato", 404)

    body = request.get_json()

    if not all(field in body for field in required_fields):
        return jsonify("Errore: Mancano uno o più campi obbligatori.", 400)

    if body["subject"] is None or body["value"] is None or body["date"] is None:
        return jsonify("Errore: I campi 'subject', 'value' e 'date' sono obbligatori e non possono essere vuoti.", 400)
        
    subject = body["subject"]
    raw_value = body["value"]
    date = body["date"]

    if not subject or raw_value is None or not date:
        return ("Errore: I campi 'subject', 'value' e 'date' sono obbligatori.", 400)

    try:
        value = float(raw_value)
    except (ValueError):
        return ("Errore: Il voto 'value' deve essere un numero valido.", 400)

    if not (0.0 <= value <= 10.0):
        return ("Errore: Il voto 'value' deve essere compreso tra 0 e 10.", 400)
    
    try:
        datetime.strptime(date, "%Y-%m-%d")
        
    except ValueError:
        return jsonify("Errore: Formato data non valido. Deve essere YYYY-MM-DD (es. 2025-10-09).", 400)

    grades = db.get("grades", [])

    new_grade = {
        "id": next_id(grades),
        "student_id": student_id,
        "subject": subject.strip(),
        "value": value,
        "date": date
    }

    db["grades"].append(new_grade)
    save_db(db)

    return jsonify(new_grade), 201

@app.post("/api/students/<int:student_id>/attendance")
def api_create_attendance(student_id):
    db = load_db()
    student = get_student(db, student_id)

    if not student:
        return ("Studente non trovato", 404)
    
    attendances = db.get("attendance", [])

    required_fields = ["date", "status"]

    body = request.get_json()

    if not all(field in body for field in required_fields):
        return jsonify("Errore: Mancano uno o più campi obbligatori.", 400)

    if body["date"] is None or body["status"] is None:
        return jsonify("Errore: I campi 'status' e 'date' sono obbligatori.", 400)

    date = body["date"]
    status = body["status"]

    new_attendance = {
        "id": next_id(attendances),
        "student_id": student_id,
        "date": date,
        "status": status,
    }

    if not status or not date:
        return ("Errore: I campi 'date' e 'status'sono obbligatori.", 400)
       
    try:
        datetime.strptime(date, "%Y-%m-%d")
        
    except ValueError:
        return jsonify("Errore: Formato data non valido. Deve essere YYYY-MM-DD (es. 2025-10-09).", 400)

    if status == statusEnum.LATE.value:
        minutes_late = body.get("minutes_late")
        if minutes_late is None:
            return ("Errore: È obbligatorio specificate i minuti di ritardo", 400)
        else:
            new_attendance["minutes_late"] = int(minutes_late)
        
    db["attendance"].append(new_attendance)
    save_db(db)

    return jsonify("Presenza creata correttamente"), 201

if __name__ == "__main__":
    app.run(debug=True)
