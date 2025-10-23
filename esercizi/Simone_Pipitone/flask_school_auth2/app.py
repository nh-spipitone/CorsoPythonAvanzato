# Importazione delle librerie necessarie da Flask e altri moduli
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash,
)  # Importa funzioni principali di Flask
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)  # Importa estensione Flask-Login per la gestione autenticazione
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)  # Per gestire hash delle password
from flask_sqlalchemy import SQLAlchemy  # ORM per database
from sqlalchemy import text  # Per eseguire query SQL raw
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)  # Per tipizzare i modelli SQLAlchemy
import json  # Per lavorare con file JSON
import os  # Per operazioni su file system
from json import JSONDecodeError  # Per gestire errori di parsing JSON
from datetime import datetime, date as _date  # Per gestire date e orari
from typing import Any, Optional  # Tipi opzionali e generici

# Imposta la directory base e il percorso del file JSON del database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory corrente del file
DB_PATH = os.path.join(BASE_DIR, "db.json")  # Percorso del file JSON con dati iniziali

# Crea l'app Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "your-secret-key-change-in-production"  # Chiave segreta per la sessione
)


# Funzione per risolvere la URI del database
def _resolve_database_uri() -> str:
    uri = os.environ.get(
        "DATABASE_URL"
    )  # Prende la variabile d'ambiente DATABASE_URL se esiste
    if uri:
        if uri.startswith("postgres://"):  # Corregge lo schema per PostgreSQL
            uri = uri.replace("postgres://", "postgresql://", 1)
        return uri
    return f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"  # Default: SQLite


# Configurazione SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = (
    _resolve_database_uri()
)  # Imposta la stringa di connessione al DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    False  # Disabilita notifiche di modifica (più efficiente)
)

# Inizializza SQLAlchemy
db = SQLAlchemy(app)  # Crea oggetto database

# ============================================
# 1: Inizializza Flask-Login
# ============================================

login_manager = LoginManager()  # Crea il gestore di login
login_manager.init_app(app)  # Inizializza con l'app Flask
login_manager.login_view = "login"  # type: ignore # Imposta la view di login
login_manager.login_message = "Per favore effettua il login per accedere a questa pagina."  # Messaggio personalizzato

# ============================================

# Database utenti fittizio (solo per esempio, non in produzione)
users_db = {
    "prof.rossi": {
        "password": generate_password_hash("prof123"),  # Password hashata
        "name": "Prof. Mario Rossi",
    },
    "segreteria": {
        "password": generate_password_hash("segreteria123"),
        "name": "Segreteria Scolastica",
    },
}


# Definizione del modello Student
class Student(db.Model):
    __tablename__ = "students"  # Nome tabella

    id: Mapped[int] = mapped_column(primary_key=True)  # Chiave primaria
    name: Mapped[str] = mapped_column(db.String(128), nullable=False)  # Nome studente
    class_name: Mapped[Optional[str]] = mapped_column("class", db.String(32))  # Classe

    grades: Mapped[list["Grade"]] = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )  # Relazione con voti
    attendance_records: Mapped[list["Attendance"]] = relationship(
        "Attendance", back_populates="student", cascade="all, delete-orphan"
    )  # Relazione con presenze

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


# Definizione del modello Grade (voto)
class Grade(db.Model):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("students.id"), nullable=False
    )  # Chiave esterna verso Student
    subject: Mapped[str] = mapped_column(db.String(128), nullable=False)  # Materia
    value: Mapped[float] = mapped_column(db.Float, nullable=False)  # Voto
    date: Mapped[_date] = mapped_column(db.Date, nullable=False)  # Data

    student = relationship("Student", back_populates="grades")  # Relazione inversa

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


# Definizione del modello Attendance (presenza)
class Attendance(db.Model):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("students.id"), nullable=False
    )  # Chiave esterna verso Student
    date: Mapped[_date] = mapped_column(db.Date, nullable=False)  # Data
    status: Mapped[str] = mapped_column(db.String(10), nullable=False)  # Stato presenza
    minutes_late: Mapped[int] = mapped_column(
        db.Integer, nullable=False, default=0
    )  # Minuti di ritardo

    student = relationship(
        "Student", back_populates="attendance_records"
    )  # Relazione inversa

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
# ============================================


class User(UserMixin):  # Eredita da UserMixin per compatibilità Flask-Login
    def __init__(self, username):
        self.id = username  # Imposta l'id come username
        self.name = users_db[username]["name"]  # Recupera il nome dal database utenti


# ============================================

# ============================================
# 3: Implementa la funzione user_loader
# ============================================


@login_manager.user_loader
def user_loader(username):
    if username in users_db:  # Controlla se l'utente esiste
        return User(username)  # Ritorna un oggetto User
    return None  # Altrimenti None


# ============================================


# Funzione di utilità per il parsing della data
def parse_date_yyyy_mm_dd(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()  # Converte stringa in data
    except Exception:
        return None  # Se errore, ritorna None


# Converte uno studente in dizionario
def _student_to_dict(student: Student) -> dict:
    return {
        "id": student.id,
        "name": student.name,
        "class": student.class_name,
    }


# Converte un voto in dizionario
def _grade_to_dict(grade: Grade) -> dict:
    return {
        "id": grade.id,
        "student_id": grade.student_id,
        "subject": grade.subject,
        "value": float(grade.value),
        "date": grade.date.isoformat() if grade.date else None,
    }


# Converte una presenza in dizionario
def _attendance_to_dict(attendance: Attendance) -> dict:
    return {
        "id": attendance.id,
        "student_id": attendance.student_id,
        "date": attendance.date.isoformat() if attendance.date else None,
        "status": attendance.status,
        "minutes_late": int(attendance.minutes_late or 0),
    }


# Calcola un riepilogo dei voti e delle presenze
def compute_summary(grades: list[dict], attendance: list[dict]) -> dict:
    avg = (
        sum(g.get("value", 0) for g in grades) / len(grades) if grades else 0.0
    )  # Media voti
    present = sum(1 for a in attendance if a.get("status") == "present")  # Presenze
    absent = sum(1 for a in attendance if a.get("status") == "absent")  # Assenze
    late = sum(1 for a in attendance if a.get("status") == "late")  # Ritardi
    minutes_late = sum(
        int(a.get("minutes_late") or 0) for a in attendance if a.get("status") == "late"
    )  # Minuti di ritardo totali
    return {
        "avg": avg,
        "count": len(grades),
        "present": present,
        "absent": absent,
        "late": late,
        "minutes_late": minutes_late,
    }


# Carica statistiche globali
def _load_stats() -> dict:
    return {
        "total_students": Student.query.count(),
        "total_grades": Grade.query.count(),
        "total_attendance": Attendance.query.count(),
    }


# Popola il database da un file JSON (se vuoto)
def _seed_data_from_json() -> None:
    if Student.query.first() is not None:
        return  # Se ci sono già studenti, non fa nulla
    if not os.path.exists(DB_PATH):
        return  # Se il file non esiste, non fa nulla
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)  # Carica dati dal file JSON
    except (OSError, JSONDecodeError):
        return  # Se errore, non fa nulla

    for student_data in raw.get("students", []):  # Inserisce studenti
        student = Student(
            id=student_data.get("id"),
            name=student_data.get("name"),
            class_name=student_data.get("class"),
        )
        db.session.add(student)

    db.session.flush()  # Salva temporaneamente per ottenere gli id

    for grade_data in raw.get("grades", []):  # Inserisce voti
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

    for attendance_data in raw.get("attendance", []):  # Inserisce presenze
        attendance_date = parse_date_yyyy_mm_dd(attendance_data.get("date", ""))
        attendance = Attendance(
            id=attendance_data.get("id"),
            student_id=attendance_data.get("student_id"),
            date=attendance_date or datetime.utcnow().date(),
            status=attendance_data.get("status"),
            minutes_late=int(attendance_data.get("minutes_late", 0)),
        )
        db.session.add(attendance)

    db.session.commit()  # Salva tutto nel database

    # Aggiorna sequenze per PostgreSQL (autoincrement id)
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
    stats = _load_stats()  # Carica statistiche
    return render_template("index.html", stats=stats)  # Mostra la homepage


@app.route("/login", methods=["GET", "POST"])
def login():
    """Route di login"""
    if current_user.is_authenticated:  # Se già autenticato, vai in dashboard
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # Recupera username e password dal form
        username = request.form["username"]
        password = request.form["password"]
        remember_me = bool(request.form.get("remember", False))
        # Verifica credenziali
        if username in users_db and check_password_hash(
            users_db[username]["password"], password
        ):
            user = User(username)
            login_user(user, remember=remember_me)  # Effettua login
            flash("Login effettuato con successo!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))  # Redirect
        else:
            flash("Credenziali non valide. Riprova.", "danger")  # Errore

    return render_template("login.html")  # Mostra form login


@app.route("/dashboard")
@login_required  # Richiede autenticazione
def dashboard():
    """Dashboard utente - Richiede autenticazione"""
    stats = _load_stats()
    return render_template("dashboard.html", name=current_user.name, stats=stats)


# ============================================
# 5: Implementa la route di logout
# ============================================


@app.route("/logout")
@login_required  # Richiede autenticazione
def logout():
    logout_user()  # Effettua logout
    return redirect(url_for("index"))  # Torna alla homepage


# ============================================

# --- Routes Gestione Studenti ---

# ============================================
# 6: Proteggi le seguenti route con @login_required
# ============================================


@app.get("/students")
@login_required  # Richiede autenticazione
def students_list():
    """Lista studenti"""
    students = [
        _student_to_dict(student)
        for student in Student.query.order_by(Student.id).all()
    ]
    return render_template("students.html", students=students)


@app.get("/students/<int:student_id>")
@login_required  # Richiede autenticazione
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
@login_required  # Richiede autenticazione
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
@login_required  # Richiede autenticazione
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
@login_required  # Richiede autenticazione
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
@login_required  # Richiede autenticazione
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


# Crea le tabelle e popola il database se necessario
with app.app_context():
    db.create_all()  # Crea le tabelle se non esistono
    _seed_data_from_json()  # Popola il database da file JSON se necessario

# Avvia l'applicazione Flask in modalità debug
if __name__ == "__main__":
    app.run(debug=True)  # Avvia il server Flask
