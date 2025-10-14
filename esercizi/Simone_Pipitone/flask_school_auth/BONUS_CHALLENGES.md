# 🏆 Esercizi Bonus - Livelli Avanzati

Hai completato l'esercizio base? Ottimo! Ecco alcune sfide aggiuntive per migliorare l'applicazione.

---

## 🥉 Livello 1: FACILE (30-45 min)

### Bonus 1.1: Validazione Password Forte

**Obiettivo**: Implementare validazione password che richieda almeno 8 caratteri, una maiuscola, un numero e un carattere speciale.

**Task**:

1. Crea una funzione di validazione:

```python
import re

def is_strong_password(password):
    """
    Valida che la password sia forte:
    - Almeno 8 caratteri
    - Almeno una maiuscola
    - Almeno un numero
    - Almeno un carattere speciale
    """
    if len(password) < 8:
        return False, "La password deve avere almeno 8 caratteri"

    if not re.search(r'[A-Z]', password):
        return False, "La password deve contenere almeno una lettera maiuscola"

    if not re.search(r'[0-9]', password):
        return False, "La password deve contenere almeno un numero"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "La password deve contenere almeno un carattere speciale"

    return True, "Password valida"
```

2. Usa la validazione nella route di registrazione (se implementi Bonus 2.1) o nel cambio password (Bonus 2.3)

**Test**:

-   Prova password deboli → Devono essere rifiutate con messaggio specifico
-   Prova "Pass123!" → Deve essere accettata

**Punti**: +10

---

### Bonus 1.2: Timestamp Ultimo Accesso

**Obiettivo**: Tracciare e mostrare quando l'utente ha effettuato l'ultimo login.

**Task**:

1. Aggiungi campo `last_login` al database utenti:

```python
users_db = {
    "prof.rossi": {
        "password": generate_password_hash("prof123"),
        "name": "Prof. Mario Rossi",
        "last_login": None  # Aggiungi questo
    }
}
```

2. Aggiorna al login:

```python
@app.route("/login", methods=["POST"])
def login():
    # ... dopo verifica credenziali corrette
    users_db[username]["last_login"] = datetime.now().isoformat()
    user = User(username)
    login_user(user)
```

3. Mostra nella dashboard:

```python
@app.route("/dashboard")
@login_required
def dashboard():
    last_login = users_db[current_user.id].get("last_login")
    if last_login:
        last_login_dt = datetime.fromisoformat(last_login)
        last_login_str = last_login_dt.strftime("%d/%m/%Y alle %H:%M")
    else:
        last_login_str = "Primo accesso"

    return render_template("dashboard.html",
                         last_login=last_login_str,
                         stats=stats)
```

**Punti**: +8

---

### Bonus 1.3: Saluto Personalizzato con Ora del Giorno

**Obiettivo**: Mostrare "Buongiorno/Buon pomeriggio/Buonasera" basato sull'ora.

**Task**:
Crea una funzione helper e usala nella dashboard:

```python
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Buongiorno"
    elif hour < 18:
        return "Buon pomeriggio"
    else:
        return "Buonasera"

@app.route("/dashboard")
@login_required
def dashboard():
    greeting = get_greeting()
    return render_template("dashboard.html",
                         greeting=greeting,
                         name=current_user.name,
                         stats=stats)
```

Template:

```html
<h1>{{ greeting }}, {{ name }}! 👋</h1>
```

**Punti**: +5

---

## 🥈 Livello 2: MEDIO (45-90 min)

### Bonus 2.0: Pagina di Registrazione (PREREQUISITO)

**Obiettivo**: Implementare una pagina di registrazione per nuovi utenti.

**Task**:

1. Il template `register.html` è già fornito
2. Crea la route `/register` in `app.py`:

```python
@app.route("/register", methods=["GET", "POST"])
def register():
    """Registrazione nuovo utente"""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "professore")

        # Validazione
        errors = []

        if not username or len(username) < 3:
            errors.append("Username deve avere almeno 3 caratteri")

        if username in users_db:
            errors.append("Username già esistente")

        if not name:
            errors.append("Nome completo obbligatorio")

        if len(password) < 8:
            errors.append("Password deve avere almeno 8 caratteri")

        if password != confirm_password:
            errors.append("Le password non coincidono")

        if role not in ["professore", "segreteria"]:
            errors.append("Ruolo non valido")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("register.html", form=request.form)

        # Crea nuovo utente
        users_db[username] = {
            "password": generate_password_hash(password),
            "name": name,
            "role": role
        }

        # Se hai implementato Bonus 2.1, salva su file
        # save_users(users_db)

        flash("Registrazione completata! Effettua il login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=None)
```

3. Aggiungi link nel template `login.html` (alla fine, prima della chiusura del div auth-card):

```html
<div style="text-align: center; margin-top: 1rem;">
    <p>
        Non hai un account? <a href="{{ url_for('register') }}">Registrati</a>
    </p>
</div>
```

**Test**:

-   Vai su `/register`
-   Prova a registrarti con username esistente → Errore
-   Prova password che non coincidono → Errore
-   Registrati con dati validi → Successo e redirect a login
-   Fai login con il nuovo account

**Punti**: +15

---

### Bonus 2.1: Persistenza Database Utenti su File JSON

**Obiettivo**: Salvare gli utenti su file JSON invece di usare un dizionario in memoria (funziona bene con Bonus 2.0).

**Task**:

1. Crea un file `users.json`:

```json
{
    "admin": {
        "password": "hash...",
        "name": "Amministratore",
        "role": "admin"
    }
}
```

2. Crea funzioni helper:

```python
USERS_PATH = os.path.join(BASE_DIR, "users.json")

def load_users():
    """Carica utenti da file JSON"""
    if not os.path.exists(USERS_PATH):
        # Crea file iniziale con utenti default
        default_users = {
            "admin": {
                "password": generate_password_hash("admin123"),
                "name": "Amministratore",
                "role": "admin"
            },
            "prof.rossi": {
                "password": generate_password_hash("prof123"),
                "name": "Prof. Mario Rossi",
                "role": "professore"
            }
        }
        save_users(default_users)
        return default_users

    with open(USERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    """Salva utenti su file JSON"""
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Carica utenti all'avvio
users_db = load_users()
```

3. Aggiorna `users_db` ogni volta che modifichi un utente e salva:

```python
# Dopo modifica password, registrazione, etc.
save_users(users_db)
```

**Test**:

-   Registra un nuovo utente
-   Riavvia l'app
-   Verifica che l'utente esista ancora

**Punti**: +20

---

### Bonus 2.2: Sistema di Ruoli Utente (Admin, Professore, Segreteria)

**Obiettivo**: Implementare ruoli con permessi diversi.

**Task**:

1. Aggiungi campo `role` agli utenti:

```python
users_db = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "name": "Amministratore",
        "role": "admin"
    },
    "prof.rossi": {
        "password": generate_password_hash("prof123"),
        "name": "Prof. Mario Rossi",
        "role": "professore"
    },
    "segreteria": {
        "password": generate_password_hash("segreteria123"),
        "name": "Segreteria Scolastica",
        "role": "segreteria"
    }
}
```

2. Aggiorna la classe `User`:

```python
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.name = users_db[username]["name"]
        self.role = users_db[username].get("role", "user")

    def is_admin(self):
        return self.role == "admin"

    def is_professore(self):
        return self.role == "professore"

    def is_segreteria(self):
        return self.role == "segreteria"
```

3. Crea decoratori custom per proteggere route:

```python
from functools import wraps

def admin_required(f):
    """Decoratore che richiede ruolo admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        if not current_user.is_admin():
            flash("Accesso negato. Solo gli amministratori possono accedere.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decoratore che richiede uno dei ruoli specificati"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("login"))
            if current_user.role not in roles:
                flash(f"Accesso negato. Ruolo richiesto: {', '.join(roles)}", "danger")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

4. Usa i decoratori:

```python
@app.route("/admin/users")
@admin_required
def admin_users():
    """Solo admin possono vedere questa pagina"""
    return render_template("admin_users.html", users=users_db)

@app.route("/students/<int:student_id>/grade/new")
@role_required("admin", "professore")
def new_grade(student_id):
    """Solo admin e professori possono aggiungere voti"""
    # ... codice esistente
```

5. Mostra ruolo nella dashboard:

```html
<div class="card">
    <h3>Il Tuo Ruolo</h3>
    <p class="metric">
        {% if current_user.is_admin() %} 🔑 Amministratore {% elif
        current_user.is_professore() %} 👨‍🏫 Professore {% else %} 📋 {{
        current_user.role }} {% endif %}
    </p>
</div>
```

**Test**:

-   Login come admin → Accedi a tutto
-   Login come prof → Accedi solo alle sue route
-   Prova ad accedere a route non permesse

**Punti**: +25

---

### Bonus 2.3: Pagina Profilo con Modifica Dati

**Obiettivo**: Permettere agli utenti di modificare nome e password.

**Task**:

1. Crea route `/profile` (GET e POST):

```python
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Pagina profilo utente"""
    if request.method == "POST":
        # Modifica nome
        new_name = request.form.get("name", "").strip()
        if new_name and new_name != current_user.name:
            users_db[current_user.id]["name"] = new_name
            save_users(users_db)  # Se usi Bonus 2.1
            flash("Nome aggiornato con successo!", "success")
            return redirect(url_for("profile"))

        # Cambio password
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if current_password and new_password:
            # Verifica password attuale
            if not check_password_hash(users_db[current_user.id]["password"], current_password):
                flash("Password attuale non corretta.", "danger")
            elif new_password != confirm_password:
                flash("Le nuove password non coincidono.", "danger")
            elif len(new_password) < 8:
                flash("La password deve avere almeno 8 caratteri.", "danger")
            else:
                # Aggiorna password
                users_db[current_user.id]["password"] = generate_password_hash(new_password)
                save_users(users_db)  # Se usi Bonus 2.1
                flash("Password aggiornata con successo!", "success")
                return redirect(url_for("profile"))

    return render_template("profile.html")
```

2. Crea template `profile.html`:

```html
{% extends "base.html" %} {% block content %}
<div class="container" style="max-width: 600px; margin-top: 2rem;">
    <h1>👤 Il Mio Profilo</h1>

    <div class="card">
        <h3>Informazioni Account</h3>
        <p><strong>Username:</strong> {{ current_user.id }}</p>
        <p><strong>Nome:</strong> {{ current_user.name }}</p>
        {% if current_user.role %}
        <p>
            <strong>Ruolo:</strong>
            <span class="badge">{{ current_user.role }}</span>
        </p>
        {% endif %}
    </div>

    <div class="card" style="margin-top: 1.5rem;">
        <h3>Modifica Profilo</h3>
        <form method="POST">
            <div class="form-group">
                <label>Nome Completo</label>
                <input
                    type="text"
                    name="name"
                    value="{{ current_user.name }}"
                    required
                />
            </div>

            <button type="submit" class="btn btn-primary">Aggiorna Nome</button>
        </form>
    </div>

    <div class="card" style="margin-top: 1.5rem;">
        <h3>Cambia Password</h3>
        <form method="POST">
            <div class="form-group">
                <label>Password Attuale</label>
                <input type="password" name="current_password" />
            </div>

            <div class="form-group">
                <label>Nuova Password</label>
                <input type="password" name="new_password" minlength="8" />
            </div>

            <div class="form-group">
                <label>Conferma Nuova Password</label>
                <input type="password" name="confirm_password" />
            </div>

            <button type="submit" class="btn btn-primary">
                Cambia Password
            </button>
        </form>
    </div>

    <div style="margin-top: 1.5rem;">
        <a href="{{ url_for('dashboard') }}" class="btn btn-secondary"
            >← Torna alla Dashboard</a
        >
    </div>
</div>
{% endblock %}
```

3. Aggiungi link nella navbar (in `base.html`):

```html
<a href="{{ url_for('profile') }}">Profilo</a>
```

**Punti**: +20

---

## 🥇 Livello 3: AVANZATO (90+ min)

### Bonus 3.1: Limitazione Tentativi di Login (Brute Force Protection)

**Obiettivo**: Bloccare temporaneamente un utente dopo 5 tentativi di login falliti.

**Task**:

1. Crea un dizionario per tracciare i tentativi:

```python
from datetime import datetime, timedelta

# Dizionario per tracciare tentativi di login
login_attempts = {}  # {username: {"count": 0, "locked_until": None, "last_attempt": None}}
```

2. Modifica la route di login:

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Controlla se l'account è bloccato
        if username in login_attempts:
            attempt = login_attempts[username]
            locked_until = attempt.get("locked_until")

            if locked_until and datetime.now() < locked_until:
                remaining_seconds = (locked_until - datetime.now()).seconds
                remaining_minutes = remaining_seconds // 60
                flash(f"Account temporaneamente bloccato. Riprova tra {remaining_minutes + 1} minuti.", "danger")
                return render_template("login.html")

        # Verifica credenziali
        if username in users_db and check_password_hash(users_db[username]["password"], password):
            # Login riuscito - resetta i tentativi
            if username in login_attempts:
                del login_attempts[username]

            user = User(username)
            login_user(user)
            flash("Login effettuato con successo!", "success")
            return redirect(url_for("dashboard"))
        else:
            # Login fallito - incrementa tentativi
            if username not in login_attempts:
                login_attempts[username] = {
                    "count": 0,
                    "locked_until": None,
                    "last_attempt": None
                }

            login_attempts[username]["count"] += 1
            login_attempts[username]["last_attempt"] = datetime.now()

            # Blocca dopo 5 tentativi
            if login_attempts[username]["count"] >= 5:
                login_attempts[username]["locked_until"] = datetime.now() + timedelta(minutes=15)
                flash("Troppi tentativi falliti. Account bloccato per 15 minuti.", "danger")
            else:
                remaining = 5 - login_attempts[username]["count"]
                flash(f"Credenziali errate. Tentativi rimasti: {remaining}", "warning")

    return render_template("login.html")
```

3. (Opzionale) Aggiungi pulizia automatica dei tentativi vecchi:

```python
def clean_old_login_attempts():
    """Rimuove tentativi di login più vecchi di 1 ora"""
    now = datetime.now()
    to_remove = []

    for username, data in login_attempts.items():
        last_attempt = data.get("last_attempt")
        if last_attempt and (now - last_attempt) > timedelta(hours=1):
            to_remove.append(username)

    for username in to_remove:
        del login_attempts[username]

# Chiama prima del controllo
@app.route("/login", methods=["GET", "POST"])
def login():
    clean_old_login_attempts()
    # ... resto del codice
```

**Test**:

-   Fai 5 login errati → Account bloccato
-   Aspetta 15 minuti (o modifica il timer per test) → Puoi riprovare
-   Login corretto → Tentativi resettati

**Punti**: +30

---

### Bonus 3.2: Log delle Attività Utente (Audit Trail)

**Obiettivo**: Registrare tutte le azioni importanti degli utenti per sicurezza e auditing.

**Task**:

1. Crea struttura per il log:

```python
import json
from datetime import datetime

ACTIVITY_LOG_PATH = os.path.join(BASE_DIR, "activity_log.json")

def load_activity_log():
    """Carica il log delle attività"""
    if not os.path.exists(ACTIVITY_LOG_PATH):
        return []
    with open(ACTIVITY_LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_activity_log(log):
    """Salva il log delle attività"""
    with open(ACTIVITY_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def log_activity(action, user=None, details=None, ip_address=None):
    """
    Registra un'attività nel log

    Args:
        action: Tipo di azione (LOGIN, LOGOUT, ADD_GRADE, etc.)
        user: Oggetto User o None
        details: Dettagli aggiuntivi (dict o str)
        ip_address: IP dell'utente
    """
    activity_log = load_activity_log()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "username": user.id if user else None,
        "user_name": user.name if user else None,
        "ip_address": ip_address or request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "details": details
    }

    activity_log.append(entry)

    # Mantieni solo gli ultimi 1000 record per non far crescere troppo il file
    if len(activity_log) > 1000:
        activity_log = activity_log[-1000:]

    save_activity_log(activity_log)
```

2. Integra il logging nelle route principali:

```python
@app.route("/login", methods=["POST"])
def login():
    # ... dopo login riuscito
    log_activity("LOGIN", user, details={"remember_me": remember})

    # ... su login fallito
    log_activity("LOGIN_FAILED", details={"username": username, "reason": "invalid_credentials"})

@app.route("/logout")
@login_required
def logout():
    log_activity("LOGOUT", current_user)
    logout_user()
    # ...

@app.post("/students/<int:student_id>/grade/new")
@login_required
def create_grade(student_id):
    # ... dopo aver creato il voto
    log_activity(
        "ADD_GRADE",
        current_user,
        details={
            "student_id": student_id,
            "student_name": student["name"],
            "subject": subject,
            "value": value
        }
    )

@app.post("/students/<int:student_id>/attendance/new")
@login_required
def create_attendance(student_id):
    # ... dopo aver creato la presenza
    log_activity(
        "ADD_ATTENDANCE",
        current_user,
        details={
            "student_id": student_id,
            "student_name": student["name"],
            "status": status,
            "date": date_s
        }
    )

@app.route("/profile", methods=["POST"])
@login_required
def profile():
    # ... dopo modifica password
    log_activity("CHANGE_PASSWORD", current_user)

    # ... dopo modifica nome
    log_activity("UPDATE_PROFILE", current_user, details={"old_name": old_name, "new_name": new_name})
```

3. Crea route per visualizzare il log (solo admin):

```python
@app.route("/admin/activity-log")
@login_required
@admin_required  # Richiede Bonus 2.2
def activity_log_view():
    """Visualizza log attività (solo admin)"""
    activity_log = load_activity_log()

    # Ordina dal più recente
    activity_log_sorted = sorted(
        activity_log,
        key=lambda x: x["timestamp"],
        reverse=True
    )

    # Limita a ultimi 100 per pagina
    page = request.args.get("page", 1, type=int)
    per_page = 100
    start = (page - 1) * per_page
    end = start + per_page

    paginated_log = activity_log_sorted[start:end]
    total_pages = (len(activity_log_sorted) + per_page - 1) // per_page

    return render_template(
        "activity_log.html",
        logs=paginated_log,
        page=page,
        total_pages=total_pages
    )
```

4. Crea template `activity_log.html`:

```html
{% extends "base.html" %} {% block content %}
<div class="container">
    <h1>📊 Log Attività Sistema</h1>

    <div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Data/Ora</th>
                    <th>Azione</th>
                    <th>Utente</th>
                    <th>IP</th>
                    <th>Dettagli</th>
                </tr>
            </thead>
            <tbody>
                {% for log in logs %}
                <tr>
                    <td>{{ log.timestamp[:19] }}</td>
                    <td>
                        <span
                            class="badge
              {% if 'LOGIN' in log.action %}badge-success
              {% elif 'LOGOUT' in log.action %}badge-secondary
              {% elif 'FAILED' in log.action %}badge-danger
              {% else %}badge-primary{% endif %}"
                        >
                            {{ log.action }}
                        </span>
                    </td>
                    <td>
                        {{ log.user_name or 'N/A' }} ({{ log.username or 'N/A'
                        }})
                    </td>
                    <td>{{ log.ip_address }}</td>
                    <td>
                        {% if log.details %} {{ log.details | tojson }} {% else
                        %} - {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Paginazione -->
    <div style="text-align: center; margin-top: 2rem;">
        {% if page > 1 %}
        <a
            href="{{ url_for('activity_log_view', page=page-1) }}"
            class="btn btn-secondary"
            >← Precedente</a
        >
        {% endif %}

        <span style="margin: 0 1rem;"
            >Pagina {{ page }} di {{ total_pages }}</span
        >

        {% if page < total_pages %}
        <a
            href="{{ url_for('activity_log_view', page=page+1) }}"
            class="btn btn-secondary"
            >Successivo →</a
        >
        {% endif %}
    </div>
</div>
{% endblock %}
```

**Test**:

-   Fai login/logout → Controlla log
-   Aggiungi voti/presenze → Verifica che siano registrati
-   Accedi come admin → Visualizza tutti i log

**Punti**: +25

---

### Bonus 3.3: Rate Limiting per API

**Obiettivo**: Limitare il numero di richieste alle API per prevenire abusi.

**Task**:

1. Crea un sistema di rate limiting semplice:

```python
from collections import defaultdict
from datetime import datetime, timedelta

# Struttura: {ip_address: {endpoint: [(timestamp1, timestamp2, ...)]}}
rate_limit_data = defaultdict(lambda: defaultdict(list))

def rate_limit(max_requests=10, window_minutes=1):
    """
    Decoratore per limitare le richieste

    Args:
        max_requests: Numero massimo di richieste
        window_minutes: Finestra temporale in minuti
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            endpoint = request.endpoint
            now = datetime.now()

            # Pulisci vecchie richieste
            cutoff = now - timedelta(minutes=window_minutes)
            rate_limit_data[ip][endpoint] = [
                ts for ts in rate_limit_data[ip][endpoint]
                if ts > cutoff
            ]

            # Controlla se ha superato il limite
            if len(rate_limit_data[ip][endpoint]) >= max_requests:
                return jsonify({
                    "error": "rate_limit_exceeded",
                    "message": f"Tropppe richieste. Limite: {max_requests} ogni {window_minutes} minuto/i."
                }), 429

            # Registra questa richiesta
            rate_limit_data[ip][endpoint].append(now)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

2. Applica alle route API:

```python
@app.get("/api/students")
@rate_limit(max_requests=30, window_minutes=1)
def api_students():
    db = load_db()
    return jsonify(db.get("students", []))

@app.get("/api/students/<int:student_id>")
@rate_limit(max_requests=60, window_minutes=1)
def api_student(student_id):
    # ... codice esistente
```

3. Aggiungi header di rate limit nelle risposte:

```python
@app.after_request
def add_rate_limit_headers(response):
    """Aggiungi header informativi sul rate limit"""
    if request.endpoint and request.endpoint.startswith("api_"):
        ip = request.remote_addr
        endpoint = request.endpoint

        # Calcola richieste rimanenti
        now = datetime.now()
        window = timedelta(minutes=1)
        cutoff = now - window

        recent_requests = [
            ts for ts in rate_limit_data[ip].get(endpoint, [])
            if ts > cutoff
        ]

        max_requests = 30  # Default
        remaining = max(0, max_requests - len(recent_requests))

        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int((cutoff + window).timestamp()))

    return response
```

4. (Avanzato) Salva rate limit su file per persistenza:

```python
def save_rate_limit_data():
    """Salva dati rate limit su file"""
    # Converti datetime in string per JSON
    serializable = {}
    for ip, endpoints in rate_limit_data.items():
        serializable[ip] = {}
        for endpoint, timestamps in endpoints.items():
            serializable[ip][endpoint] = [ts.isoformat() for ts in timestamps]

    with open("rate_limit_data.json", "w") as f:
        json.dump(serializable, f)

def load_rate_limit_data():
    """Carica dati rate limit da file"""
    try:
        with open("rate_limit_data.json", "r") as f:
            data = json.load(f)

        # Converti string in datetime
        for ip, endpoints in data.items():
            for endpoint, timestamps in endpoints.items():
                rate_limit_data[ip][endpoint] = [
                    datetime.fromisoformat(ts) for ts in timestamps
                ]
    except FileNotFoundError:
        pass

# Carica all'avvio
load_rate_limit_data()

# Salva periodicamente o alla chiusura
import atexit
atexit.register(save_rate_limit_data)
```

**Test**:

-   Fai molte richieste rapide alle API
-   Verifica che dopo il limite ricevi errore 429
-   Controlla gli header X-RateLimit-\*

**Punti**: +30

---

### Bonus 3.4: Session Management Avanzato

**Obiettivo**: Gestire sessioni multiple, visualizzarle e permettere di revocarle.

**Task**:

1. Crea struttura per tracciare le sessioni:

```python
# Struttura: {username: [{session_id, login_time, last_seen, ip, user_agent, is_current}]}
user_sessions = defaultdict(list)

def get_session_id():
    """Genera un ID univoco per la sessione"""
    import uuid
    return str(uuid.uuid4())
```

2. Registra sessione al login:

```python
@app.route("/login", methods=["POST"])
def login():
    # ... dopo login riuscito
    session_id = get_session_id()
    session["session_id"] = session_id

    user_sessions[username].append({
        "session_id": session_id,
        "login_time": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat(),
        "ip_address": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "is_current": True
    })

    login_user(user)
    # ...
```

3. Aggiorna last_seen ad ogni richiesta:

```python
@app.before_request
def update_last_seen():
    """Aggiorna timestamp ultimo accesso della sessione"""
    if current_user.is_authenticated and "session_id" in session:
        username = current_user.id
        session_id = session["session_id"]

        # Trova e aggiorna la sessione
        for sess in user_sessions[username]:
            if sess["session_id"] == session_id:
                sess["last_seen"] = datetime.now().isoformat()
                break
```

4. Crea pagina per visualizzare sessioni attive:

```python
@app.route("/profile/sessions")
@login_required
def profile_sessions():
    """Visualizza tutte le sessioni attive dell'utente"""
    sessions = user_sessions[current_user.id]
    current_session_id = session.get("session_id")

    # Marca la sessione corrente
    for sess in sessions:
        sess["is_current"] = sess["session_id"] == current_session_id

        # Formatta date
        login_time = datetime.fromisoformat(sess["login_time"])
        last_seen = datetime.fromisoformat(sess["last_seen"])

        sess["login_time_formatted"] = login_time.strftime("%d/%m/%Y %H:%M")
        sess["last_seen_formatted"] = last_seen.strftime("%d/%m/%Y %H:%M")

        # Calcola durata
        duration = datetime.now() - last_seen
        if duration.seconds < 60:
            sess["last_seen_relative"] = "Adesso"
        elif duration.seconds < 3600:
            minutes = duration.seconds // 60
            sess["last_seen_relative"] = f"{minutes} minuti fa"
        elif duration.days == 0:
            hours = duration.seconds // 3600
            sess["last_seen_relative"] = f"{hours} ore fa"
        else:
            sess["last_seen_relative"] = f"{duration.days} giorni fa"

    return render_template("sessions.html", sessions=sessions)
```

5. Permetti di revocare sessioni:

```python
@app.route("/profile/sessions/<session_id>/revoke", methods=["POST"])
@login_required
def revoke_session(session_id):
    """Revoca una sessione specifica"""
    username = current_user.id

    # Rimuovi la sessione
    user_sessions[username] = [
        sess for sess in user_sessions[username]
        if sess["session_id"] != session_id
    ]

    flash("Sessione revocata con successo.", "success")
    log_activity("REVOKE_SESSION", current_user, details={"session_id": session_id})

    return redirect(url_for("profile_sessions"))

@app.route("/profile/sessions/revoke-all", methods=["POST"])
@login_required
def revoke_all_sessions():
    """Revoca tutte le sessioni tranne quella corrente"""
    username = current_user.id
    current_session_id = session.get("session_id")

    # Mantieni solo la sessione corrente
    user_sessions[username] = [
        sess for sess in user_sessions[username]
        if sess["session_id"] == current_session_id
    ]

    flash("Tutte le altre sessioni sono state revocate.", "success")
    log_activity("REVOKE_ALL_SESSIONS", current_user)

    return redirect(url_for("profile_sessions"))
```

6. Crea template `sessions.html`:

```html
{% extends "base.html" %} {% block content %}
<div class="container" style="max-width: 800px;">
    <h1>🔒 Le Tue Sessioni Attive</h1>

    <div class="alert alert-info">
        <strong>Info:</strong> Puoi vedere tutti i dispositivi dove sei
        attualmente loggato e revocare l'accesso.
    </div>

    {% if sessions %}
    <div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Dispositivo</th>
                    <th>IP</th>
                    <th>Login</th>
                    <th>Ultimo Accesso</th>
                    <th>Azioni</th>
                </tr>
            </thead>
            <tbody>
                {% for sess in sessions %}
                <tr
                    {%
                    if
                    sess.is_current
                    %}style="background-color: #f0f9ff;"
                    {%
                    endif
                    %}
                >
                    <td>
                        {% if 'Mobile' in sess.user_agent %}📱{% elif 'Tablet'
                        in sess.user_agent %}📱{% else %}💻{% endif %} {{
                        sess.user_agent[:50] }}... {% if sess.is_current %}
                        <br /><span class="badge badge-success"
                            >Sessione Corrente</span
                        >
                        {% endif %}
                    </td>
                    <td>{{ sess.ip_address }}</td>
                    <td>{{ sess.login_time_formatted }}</td>
                    <td>{{ sess.last_seen_relative }}</td>
                    <td>
                        {% if not sess.is_current %}
                        <form
                            method="POST"
                            action="{{ url_for('revoke_session', session_id=sess.session_id) }}"
                            style="display: inline;"
                        >
                            <button
                                type="submit"
                                class="btn btn-small"
                                style="background: var(--danger);"
                                onclick="return confirm('Vuoi revocare questa sessione?')"
                            >
                                Revoca
                            </button>
                        </form>
                        {% else %}
                        <span style="color: var(--text-light);">Attiva</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    {% if sessions|length > 1 %}
    <div style="margin-top: 2rem; text-align: center;">
        <form
            method="POST"
            action="{{ url_for('revoke_all_sessions') }}"
            style="display: inline;"
        >
            <button
                type="submit"
                class="btn"
                style="background: var(--danger);"
                onclick="return confirm('Vuoi revocare tutte le altre sessioni?')"
            >
                🚫 Revoca Tutte le Altre Sessioni
            </button>
        </form>
    </div>
    {% endif %} {% else %}
    <p class="empty-state">Nessuna sessione attiva</p>
    {% endif %}

    <div style="margin-top: 2rem;">
        <a href="{{ url_for('profile') }}" class="btn btn-secondary"
            >← Torna al Profilo</a
        >
    </div>
</div>
{% endblock %}
```

7. Valida sessione ad ogni richiesta:

```python
@app.before_request
def validate_session():
    """Controlla che la sessione sia ancora valida"""
    if current_user.is_authenticated and "session_id" in session:
        username = current_user.id
        session_id = session["session_id"]

        # Verifica che la sessione esista ancora
        valid_session_ids = [sess["session_id"] for sess in user_sessions[username]]

        if session_id not in valid_session_ids:
            # Sessione revocata - logout
            logout_user()
            flash("La tua sessione è stata revocata.", "warning")
            return redirect(url_for("login"))
```

**Test**:

-   Login da browser normale
-   Login da incognito → Vedi 2 sessioni
-   Revoca sessione incognito dal browser normale
-   Verifica che incognito venga disconnesso

**Punti**: +35

---

## 📊 Tabella Riepilogativa Punti

| Bonus                          | Livello  | Tempo   | Punti    |
| ------------------------------ | -------- | ------- | -------- |
| 1.1 Validazione Password Forte | Facile   | 30 min  | +10      |
| 1.2 Timestamp Ultimo Accesso   | Facile   | 25 min  | +8       |
| 1.3 Saluto Personalizzato      | Facile   | 15 min  | +5       |
| 2.1 Persistenza JSON           | Medio    | 60 min  | +20      |
| 2.2 Sistema Ruoli              | Medio    | 75 min  | +25      |
| 2.3 Pagina Profilo             | Medio    | 60 min  | +20      |
| 3.1 Limita Tentativi           | Avanzato | 90 min  | +30      |
| 3.2 Log Attività               | Avanzato | 90 min  | +25      |
| 3.3 Rate Limiting              | Avanzato | 90 min  | +30      |
| 3.4 Session Management         | Avanzato | 120 min | +35      |
| **TOTALE POSSIBILE**           |          |         | **+208** |

---

## 🎯 Suggerimenti per il Docente

### Assegnazione Progressiva:

1. Studenti che finiscono in anticipo → Livello 1
2. Studenti molto veloci → Livello 2
3. Studenti eccellenti che vogliono sfidarsi → Livello 3

### Valutazione:

-   **Eccellente (110%)**: Esercizio base + almeno 2 bonus livello medio
-   **Ottimo (100%)**: Esercizio base completato perfettamente
-   **Buono (90%)**: Esercizio base con piccoli errori

### Combinazioni Consigliate:

-   **Path Sicurezza**: 3.1 (Brute Force) + 3.2 (Log Attività) + 3.3 (Rate Limiting)
-   **Path Backend Avanzato**: 2.1 (Persistenza JSON) + 2.2 (Ruoli) + 3.4 (Session Management)
-   **Path Completo**: 1.1 (Validazione) + 1.2 (Timestamp) + 2.2 (Ruoli) + 2.3 (Profilo) + 3.1 (Brute Force) + 3.2 (Log)

---

## 💡 Note

-   Non è necessario completare tutti i bonus
-   Scegli quelli che ti interessano di più
-   Testa sempre dopo ogni modifica
-   Chiedi aiuto se ti blocchi
-   Divertiti a migliorare l'app! 🚀

**Buon lavoro! 💪**
