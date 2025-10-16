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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import json
import os
from json import JSONDecodeError
from datetime import datetime, date as _date
from typing import Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.json")

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-change-in-production"


def _resolve_database_uri() -> str:
    uri = os.environ.get("DATABASE_URL")
    if uri:
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        return uri
    return f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"


app.config["SQLALCHEMY_DATABASE_URI"] = _resolve_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ============================================
# 1: Inizializza Flask-Login
# - Crea un'istanza di LoginManager
# - Inizializzala con l'app Flask
# - Imposta login_view su "login"
# - Imposta un messaggio personalizzato per login_message
# ============================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # type: ignore[assignment]
login_manager.login_message = (
    "Per favore effettua il login per accedere a questa pagina."
)


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


class Student(db.Model):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(128), nullable=False)
    class_name: Mapped[Optional[str]] = mapped_column("class", db.String(32))

    grades: Mapped[list["Grade"]] = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )
    attendance_records: Mapped[list["Attendance"]] = relationship(
        "Attendance", back_populates="student", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        *,
        id: int | None = None,
        name: str,
        class_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        self.name = name
        self.class_name = class_name


class Grade(db.Model):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("students.id"), nullable=False
    )
    subject: Mapped[str] = mapped_column(db.String(128), nullable=False)
    value: Mapped[float] = mapped_column(db.Float, nullable=False)
    date: Mapped[_date] = mapped_column(db.Date, nullable=False)

    student = relationship("Student", back_populates="grades")

    def __init__(
        self,
        *,
        id: int | None = None,
        student_id: int,
        subject: str,
        value: float,
        date: _date,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = date


class Attendance(db.Model):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("students.id"), nullable=False
    )
    date: Mapped[_date] = mapped_column(db.Date, nullable=False)
    status: Mapped[str] = mapped_column(db.String(10), nullable=False)
    minutes_late: Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)

    student = relationship("Student", back_populates="attendance_records")

    def __init__(
        self,
        *,
        id: int | None = None,
        student_id: int,
        date: _date,
        status: str,
        minutes_late: int = 0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        self.student_id = student_id
        self.date = date
        self.status = status
        self.minutes_late = minutes_late


# ============================================
#  2: Implementa la classe User
# - Deve ereditare da UserMixin
# - Deve avere un costruttore che accetta username
# - Deve impostare self.id con lo username
# - Deve impostare self.name dal database users_db
# ============================================


# SCRIVI IL TUO CODICE QUI
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.name = users_db[username]["name"]


# ============================================


# ============================================
# 3: Implementa la funzione user_loader
# - Usa il decoratore @login_manager.user_loader
# - Controlla se username esiste in users_db
# - Ritorna un oggetto User se esiste, None altrimenti
# ============================================


# SCRIVI IL TUO CODICE QUI
@login_manager.user_loader
def user_loader(username):
    if username in users_db:
        return User(username)
    return None


# ============================================


def parse_date_yyyy_mm_dd(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def _student_to_dict(student: Student) -> dict:
    return {
        "id": student.id,
        "name": student.name,
        "class": student.class_name,
    }


def _grade_to_dict(grade: Grade) -> dict:
    return {
        "id": grade.id,
        "student_id": grade.student_id,
        "subject": grade.subject,
        "value": float(grade.value),
        "date": grade.date.isoformat() if grade.date else None,
    }


def _attendance_to_dict(attendance: Attendance) -> dict:
    return {
        "id": attendance.id,
        "student_id": attendance.student_id,
        "date": attendance.date.isoformat() if attendance.date else None,
        "status": attendance.status,
        "minutes_late": int(attendance.minutes_late or 0),
    }


def compute_summary(grades: list[dict], attendance: list[dict]) -> dict:
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


def _load_stats() -> dict:
    return {
        "total_students": Student.query.count(),
        "total_grades": Grade.query.count(),
        "total_attendance": Attendance.query.count(),
    }


def _seed_data_from_json() -> None:
    if Student.query.first() is not None:
        return
    if not os.path.exists(DB_PATH):
        return
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, JSONDecodeError):
        return

    for student_data in raw.get("students", []):
        student = Student(
            id=student_data.get("id"),
            name=student_data.get("name"),
            class_name=student_data.get("class"),
        )
        db.session.add(student)

    db.session.flush()

    for grade_data in raw.get("grades", []):
        grade_date = parse_date_yyyy_mm_dd(grade_data.get("date", ""))
        grade = Grade(
            id=grade_data.get("id"),
            student_id=grade_data.get("student_id"),
            subject=grade_data.get("subject"),
            value=float(grade_data.get("value", 0)),
            date=grade_date or datetime.utcnow().date(),
        )
        db.session.add(grade)

    db.session.flush()

    for attendance_data in raw.get("attendance", []):
        attendance_date = parse_date_yyyy_mm_dd(attendance_data.get("date", ""))
        attendance = Attendance(
            id=attendance_data.get("id"),
            student_id=attendance_data.get("student_id"),
            date=attendance_date or datetime.utcnow().date(),
            status=attendance_data.get("status"),
            minutes_late=int(attendance_data.get("minutes_late", 0)),
        )
        db.session.add(attendance)

    db.session.commit()

    if db.engine.dialect.name == "postgresql":
        tables = (
            Student.__tablename__,
            Grade.__tablename__,
            Attendance.__tablename__,
        )
        for table_name in tables:
            sql = text(
                "SELECT setval(pg_get_serial_sequence(:table_name, 'id'), "
                "COALESCE((SELECT MAX(id) FROM " + table_name + "), 1))"
            )
            db.session.execute(sql, {"table_name": table_name})
        db.session.commit()


# --- Routes Autenticazione ---


@app.route("/")
def index():
    """Homepage pubblica - NON richiede autenticazione"""
    stats = _load_stats()
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

        username = request.form["username"]
        password = request.form["password"]
        remember_me = bool(request.form.get("remember", False))
        if username in users_db and check_password_hash(
            users_db[username]["password"], password
        ):
            user = User(username)
            login_user(user, remember=remember_me)
            flash("Login effettuato con successo!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        else:
            flash("Credenziali non valide. Riprova.", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard utente - Richiede autenticazione"""
    stats = _load_stats()
    return render_template("dashboard.html", name=current_user.name, stats=stats)


# ============================================
# TODO 5: Implementa la route di logout
# - Usa il decoratore @login_required
# - Chiama logout_user()
# - Redirect alla homepage
# ============================================


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# ============================================


# --- Routes Gestione Studenti ---

# ============================================
# TODO 6: Proteggi le seguenti route con @login_required
# Aggiungi il decoratore @login_required PRIMA di ogni route
# ============================================


@app.get("/students")
@login_required
def students_list():
    """Lista studenti"""
    students = [
        _student_to_dict(student)
        for student in Student.query.order_by(Student.id).all()
    ]
    return render_template("students.html", students=students)


@app.get("/students/<int:student_id>")
@login_required
def student_detail(student_id):
    """Dettaglio studente"""
    student = Student.query.get(student_id)
    if not student:
        return ("Studente non trovato", 404)

    grades_records = (
        Grade.query.filter_by(student_id=student_id)
        .order_by(Grade.date.desc(), Grade.id.desc())
        .all()
    )
    grades = [_grade_to_dict(grade) for grade in grades_records]

    attendance_records = (
        Attendance.query.filter_by(student_id=student_id)
        .order_by(Attendance.date.desc(), Attendance.id.desc())
        .all()
    )
    attendance = [_attendance_to_dict(record) for record in attendance_records]

    summary = compute_summary(grades, attendance)
    return render_template(
        "student_detail.html",
        student=_student_to_dict(student),
        grades=grades,
        attendance=attendance,
        summary=summary,
    )


@app.get("/students/<int:student_id>/grade/new")
@login_required
def new_grade(student_id):
    """Form nuovo voto"""
    student = Student.query.get(student_id)
    if not student:
        return ("Studente non trovato", 404)
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template(
        "form_grade.html",
        student=_student_to_dict(student),
        errors=[],
        form={"subject": "", "value": "", "date": today},
    )


@app.post("/students/<int:student_id>/grade/new")
@login_required
def create_grade(student_id):
    """Crea nuovo voto"""
    student = Student.query.get(student_id)
    if not student:
        return ("Studente non trovato", 404)

    subject = (request.form.get("subject") or "").strip()
    value_raw = (request.form.get("value") or "").strip()
    date_s = (request.form.get("date") or "").strip()

    errors = []
    if not subject:
        errors.append("La materia è obbligatoria.")
    value: float | None = None
    try:
        value = float(value_raw)
        if not (0 <= value <= 10):
            errors.append("Il voto deve essere tra 0 e 10.")
    except ValueError:
        errors.append("Il voto deve essere numerico.")
        value = None

    grade_date = parse_date_yyyy_mm_dd(date_s)
    if not grade_date:
        errors.append("Data non valida. Usa formato YYYY-MM-DD.")

    if errors:
        return (
            render_template(
                "form_grade.html",
                student=_student_to_dict(student),
                errors=errors,
                form={"subject": subject, "value": value_raw, "date": date_s},
            ),
            400,
        )

    assert value is not None
    assert grade_date is not None

    grade = Grade(
        student_id=student_id,
        subject=subject,
        value=value,
        date=grade_date,
    )
    db.session.add(grade)
    db.session.commit()
    return redirect(url_for("student_detail", student_id=student_id))


@app.get("/students/<int:student_id>/attendance/new")
@login_required
def new_attendance(student_id):
    """Form nuova presenza"""
    student = Student.query.get(student_id)
    if not student:
        return ("Studente non trovato", 404)
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template(
        "form_attendance.html",
        student=_student_to_dict(student),
        errors=[],
        form={"date": today, "status": "", "minutes_late": ""},
    )


@app.post("/students/<int:student_id>/attendance/new")
@login_required
def create_attendance(student_id):
    """Crea nuova presenza"""
    student = Student.query.get(student_id)
    if not student:
        return ("Studente non trovato", 404)

    date_s = (request.form.get("date") or "").strip()
    status = (request.form.get("status") or "").strip()
    minutes_raw = (request.form.get("minutes_late") or "").strip()

    errors = []
    attendance_date = parse_date_yyyy_mm_dd(date_s)
    if not attendance_date:
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
                student=_student_to_dict(student),
                errors=errors,
                form={"date": date_s, "status": status, "minutes_late": minutes_raw},
            ),
            400,
        )

    assert attendance_date is not None

    attendance = Attendance(
        student_id=student_id,
        date=attendance_date,
        status=status,
        minutes_late=minutes if status == "late" else 0,
    )
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for("student_detail", student_id=student_id))


# --- API Routes (Opzionali - Non richiedono autenticazione per semplicità) ---


@app.get("/api/students")
def api_students():
    students = [
        _student_to_dict(student)
        for student in Student.query.order_by(Student.id).all()
    ]
    return jsonify(students)


@app.get("/api/students/<int:student_id>")
def api_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify(error="not_found"), 404
    grades = [
        _grade_to_dict(grade)
        for grade in Grade.query.filter_by(student_id=student_id).all()
    ]
    attendance = [
        _attendance_to_dict(record)
        for record in Attendance.query.filter_by(student_id=student_id).all()
    ]
    return jsonify(
        {
            "student": _student_to_dict(student),
            "grades": grades,
            "attendance": attendance,
        }
    )


with app.app_context():
    db.create_all()
    _seed_data_from_json()


if __name__ == "__main__":
    app.run(debug=True)
