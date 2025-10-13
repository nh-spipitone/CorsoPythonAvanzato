from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import os, json
from json import JSONDecodeError
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.json")

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-change-in-production"

# ============================================
# TODO 1: Inizializza Flask-Login
# - Crea un'istanza di LoginManager
# - Inizializzala con l'app Flask
# - Imposta login_view su "login"
# - Imposta un messaggio personalizzato per login_message
# ============================================

# SCRIVI IL TUO CODICE QUI


# ============================================

# Database utenti (in produzione usare un vero database)
users_db = {
    "prof.rossi": {
        "password": generate_password_hash("prof123"),
        "name": "Prof. Mario Rossi",
    },
    "segreteria": {
        "password": generate_password_hash("segreteria123"),
        "name": "Segreteria Scolastica",
    },
}


# ============================================
# TODO 2: Implementa la classe User
# - Deve ereditare da UserMixin
# - Deve avere un costruttore che accetta username
# - Deve impostare self.id con lo username
# - Deve impostare self.name dal database users_db
# ============================================

# SCRIVI IL TUO CODICE QUI


# ============================================


# ============================================
# TODO 3: Implementa la funzione user_loader
# - Usa il decoratore @login_manager.user_loader
# - Controlla se username esiste in users_db
# - Ritorna un oggetto User se esiste, None altrimenti
# ============================================

# SCRIVI IL TUO CODICE QUI


# ============================================


# --- Database Helpers (NON MODIFICARE) ---
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
            data.setdefault("students", [])
            data.setdefault("grades", [])
            data.setdefault("attendance", [])
            return data
    except (JSONDecodeError, OSError):
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
    attendance = [
        a for a in db.get("attendance", []) if a.get("student_id") == student_id
    ]
    avg = sum(g.get("value", 0) for g in grades) / len(grades) if grades else 0.0
    present = sum(1 for a in attendance if a.get("status") == "present")
    absent = sum(1 for a in attendance if a.get("status") == "absent")
    late = sum(1 for a in attendance if a.get("status") == "late")
    minutes_late = sum(
        int(a.get("minutes_late") or 0) for a in attendance if a.get("status") == "late"
    )
    return {
        "avg": avg,
        "count": len(grades),
        "present": present,
        "absent": absent,
        "late": late,
        "minutes_late": minutes_late,
    }


# --- Routes Autenticazione ---


@app.route("/")
def index():
    """Homepage pubblica - NON richiede autenticazione"""
    db = load_db()
    stats = {
        "total_students": len(db.get("students", [])),
        "total_grades": len(db.get("grades", [])),
        "total_attendance": len(db.get("attendance", [])),
    }
    return render_template("index.html", stats=stats)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Route di login"""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # ============================================
        # TODO 4: Implementa la logica di login POST
        # - Recupera username e password dal form
        # - Verifica se l'utente esiste nel database
        # - Verifica la password con check_password_hash
        # - Se corrette: login_user() e redirect a dashboard
        # - Se errate: flash message di errore e resta su login
        # ============================================

        # SCRIVI IL TUO CODICE QUI

        # ============================================
        pass

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard utente - Richiede autenticazione"""
    db = load_db()
    stats = {
        "total_students": len(db.get("students", [])),
        "total_grades": len(db.get("grades", [])),
        "total_attendance": len(db.get("attendance", [])),
    }
    return render_template("dashboard.html", name=current_user.name, stats=stats)


# ============================================
# TODO 5: Implementa la route di logout
# - Usa il decoratore @login_required
# - Chiama logout_user()
# - Redirect alla homepage
# ============================================

# SCRIVI IL TUO CODICE QUI


# ============================================


# --- Routes Gestione Studenti ---

# ============================================
# TODO 6: Proteggi le seguenti route con @login_required
# Aggiungi il decoratore @login_required PRIMA di ogni route
# ============================================


@app.get("/students")
def students_list():
    """Lista studenti"""
    db = load_db()
    return render_template("students.html", students=db.get("students", []))


@app.get("/students/<int:student_id>")
def student_detail(student_id):
    """Dettaglio studente"""
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    grades = [g for g in db.get("grades", []) if g.get("student_id") == student_id]
    grades = sorted(
        grades, key=lambda g: (g.get("date") or "", g.get("id", 0)), reverse=True
    )
    attendance = [
        a for a in db.get("attendance", []) if a.get("student_id") == student_id
    ]
    attendance = sorted(
        attendance, key=lambda a: (a.get("date") or "", a.get("id", 0)), reverse=True
    )
    summary = compute_summary(db, student_id)
    return render_template(
        "student_detail.html",
        student=student,
        grades=grades,
        attendance=attendance,
        summary=summary,
    )


@app.get("/students/<int:student_id>/grade/new")
def new_grade(student_id):
    """Form nuovo voto"""
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template(
        "form_grade.html",
        student=student,
        errors=[],
        form={"subject": "", "value": "", "date": today},
    )


@app.post("/students/<int:student_id>/grade/new")
def create_grade(student_id):
    """Crea nuovo voto"""
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
        return (
            render_template(
                "form_grade.html",
                student=student,
                errors=errors,
                form={"subject": subject, "value": value_raw, "date": date_s},
            ),
            400,
        )

    grade = {
        "id": next_id(db["grades"]),
        "student_id": student_id,
        "subject": subject,
        "value": value,
        "date": date_s,
    }
    db["grades"].append(grade)
    save_db(db)
    return redirect(url_for("student_detail", student_id=student_id))


@app.get("/students/<int:student_id>/attendance/new")
def new_attendance(student_id):
    """Form nuova presenza"""
    db = load_db()
    student = get_student(db, student_id)
    if not student:
        return ("Studente non trovato", 404)
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template(
        "form_attendance.html",
        student=student,
        errors=[],
        form={"date": today, "status": "", "minutes_late": ""},
    )


@app.post("/students/<int:student_id>/attendance/new")
def create_attendance(student_id):
    """Crea nuova presenza"""
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
        return (
            render_template(
                "form_attendance.html",
                student=student,
                errors=errors,
                form={"date": date_s, "status": status, "minutes_late": minutes_raw},
            ),
            400,
        )

    att = {
        "id": next_id(db["attendance"]),
        "student_id": student_id,
        "date": date_s,
        "status": status,
        "minutes_late": minutes if status == "late" else 0,
    }
    db["attendance"].append(att)
    save_db(db)
    return redirect(url_for("student_detail", student_id=student_id))


# --- API Routes (Opzionali - Non richiedono autenticazione per semplicità) ---


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
    attendance = [
        a for a in db.get("attendance", []) if a.get("student_id") == student_id
    ]
    return jsonify({"student": student, "grades": grades, "attendance": attendance})


if __name__ == "__main__":
    app.run(debug=True)
