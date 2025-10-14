"""
ESERCIZIO: TASK MANAGER CON BEARER TOKEN AUTHENTICATION
========================================================
Crea un'applicazione completa per gestire task personali con autenticazione.

FUNZIONALITÀ:
- Registrazione e Login utenti
- Autenticazione con Bearer Token (salvato in session)
- CRUD completo per i task (Create, Read, Update, Delete)
- Ogni utente vede solo i propri task
- Filtri: task completati/da fare
- Statistiche personali

OBIETTIVI DI APPRENDIMENTO:
- Implementare sistema di autenticazione completo
- Gestire dati utente separati
- CRUD operations con protezione
- Session management
- Template inheritance
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

# =============================================================================
# TODO 1: CONFIGURAZIONE
# =============================================================================
# Imposta la SECRET_KEY per le sessioni usando secrets.token_hex(16)
app.config["SECRET_KEY"] = None  # <-- IMPLEMENTA QUI

# Durata del token (30 minuti)
TOKEN_EXPIRATION = None  # <-- IMPLEMENTA QUI (timedelta)


# =============================================================================
# TODO 2: DATABASE SIMULATO
# =============================================================================
# Crea le seguenti strutture dati:

# USERS: dizionario {username: password}
# Esempio: {"mario": "pass123", "lucia": "secret456"}
USERS = {}  # <-- IMPLEMENTA QUI

# ACTIVE_TOKENS: {token: {"username": str, "expires": datetime, "created": datetime}}
ACTIVE_TOKENS = {}  # <-- IMPLEMENTA QUI

# TASKS: lista di task, ogni task è un dizionario:
# {
#   "id": int (univoco),
#   "username": str (proprietario),
#   "title": str,
#   "description": str,
#   "completed": bool,
#   "created_at": datetime,
#   "completed_at": datetime o None
# }
TASKS = []  # <-- IMPLEMENTA QUI

# Contatore per ID task univoci
TASK_ID_COUNTER = 1


# =============================================================================
# TODO 3: FUNZIONI HELPER PER TOKEN
# =============================================================================


def generate_token():
    """Genera un token Bearer sicuro."""
    # TODO 3a: Usa secrets.token_urlsafe(32)
    pass  # <-- IMPLEMENTA QUI


def create_token(username):
    """Crea e memorizza un nuovo token per l'utente."""
    # TODO 3b:
    # 1. Genera token con generate_token()
    # 2. Salvalo in ACTIVE_TOKENS con username, expires, created
    # 3. Restituisci il token
    pass  # <-- IMPLEMENTA QUI


def verify_token(token):
    """Verifica validità del token."""
    # TODO 3c:
    # 1. Controlla se esiste in ACTIVE_TOKENS
    # 2. Verifica scadenza
    # 3. Se scaduto, rimuovilo
    # 4. Restituisci username se valido, None altrimenti
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 4: DECORATOR PER PROTEZIONE
# =============================================================================


def login_required(f):
    """Decorator per proteggere le route."""
    # TODO 4a:
    # 1. Controlla se 'token' è in session
    # 2. Se no, flash errore e redirect a login
    # 3. Verifica token con verify_token()
    # 4. Se non valido, rimuovi da session, flash errore, redirect login
    # 5. Se valido, chiama funzione passando current_user=username

    @wraps(f)
    def decorated(*args, **kwargs):
        pass  # <-- IMPLEMENTA QUI

    return decorated


# =============================================================================
# TODO 5: FUNZIONI HELPER PER TASK
# =============================================================================


def get_user_tasks(username, filter_completed=None):
    """Ottieni i task di un utente."""
    # TODO 5a:
    # 1. Filtra TASKS per username
    # 2. Se filter_completed è True, solo completati
    # 3. Se filter_completed è False, solo non completati
    # 4. Se None, tutti i task
    # 5. Restituisci lista task
    pass  # <-- IMPLEMENTA QUI


def get_task_by_id(task_id, username):
    """Ottieni un task specifico (solo se appartiene all'utente)."""
    # TODO 5b:
    # 1. Cerca task in TASKS con id == task_id
    # 2. Verifica che username corrisponda
    # 3. Restituisci task o None
    pass  # <-- IMPLEMENTA QUI


def create_task(username, title, description=""):
    """Crea un nuovo task."""
    # TODO 5c:
    # 1. Usa TASK_ID_COUNTER globale per id univoco
    # 2. Crea dizionario task con tutti i campi
    # 3. Aggiungi a TASKS
    # 4. Incrementa TASK_ID_COUNTER
    # 5. Restituisci il task creato
    pass  # <-- IMPLEMENTA QUI


def update_task(task_id, username, title=None, description=None, completed=None):
    """Aggiorna un task esistente."""
    # TODO 5d:
    # 1. Trova task con get_task_by_id()
    # 2. Se non esiste o non appartiene all'utente, return False
    # 3. Aggiorna campi se forniti
    # 4. Se completed diventa True, imposta completed_at
    # 5. Return True
    pass  # <-- IMPLEMENTA QUI


def delete_task(task_id, username):
    """Elimina un task."""
    # TODO 5e:
    # 1. Trova task con get_task_by_id()
    # 2. Se non esiste o non appartiene all'utente, return False
    # 3. Rimuovi da TASKS
    # 4. Return True
    pass  # <-- IMPLEMENTA QUI


def get_user_stats(username):
    """Ottieni statistiche utente."""
    # TODO 5f:
    # 1. Conta task totali dell'utente
    # 2. Conta task completati
    # 3. Conta task da fare
    # 4. Restituisci dizionario con le statistiche
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# ROUTE PUBBLICHE
# =============================================================================


@app.route("/")
def index():
    """Homepage."""
    is_logged_in = "token" in session and verify_token(session["token"]) is not None
    return render_template("index.html", is_logged_in=is_logged_in)


# =============================================================================
# TODO 6: ROUTE REGISTRAZIONE
# =============================================================================


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registrazione nuovo utente."""
    # TODO 6a:
    # GET: mostra template 'register.html'
    # POST:
    #   1. Ottieni username e password da request.form
    #   2. Valida: username non vuoto, password min 6 caratteri
    #   3. Verifica che username non esista già in USERS
    #   4. Aggiungi utente a USERS
    #   5. Flash messaggio successo
    #   6. Redirect a login
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 7: ROUTE LOGIN
# =============================================================================


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login utente."""
    # TODO 7a:
    # GET: mostra template 'login.html'
    # POST:
    #   1. Ottieni username e password da request.form
    #   2. Verifica credenziali contro USERS
    #   3. Se valide: crea token, salva in session, redirect a dashboard
    #   4. Se non valide: flash errore, rimostra form
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 8: ROUTE LOGOUT
# =============================================================================


@app.route("/logout")
def logout():
    """Logout utente."""
    # TODO 8a:
    # 1. Ottieni token da session
    # 2. Rimuovilo da ACTIVE_TOKENS se esiste
    # 3. Rimuovi da session
    # 4. Flash messaggio
    # 5. Redirect a index
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 9: ROUTE DASHBOARD (PROTETTA)
# =============================================================================


@app.route("/dashboard")
# @login_required  # <-- DECOMMENTA
def dashboard(current_user=None):
    """Dashboard principale con lista task."""
    # TODO 9a:
    # 1. Ottieni filtro da request.args.get('filter')
    #    (può essere 'completed', 'todo', o None per tutti)
    # 2. Converti filtro in booleano per get_user_tasks()
    # 3. Ottieni task con get_user_tasks()
    # 4. Ottieni stats con get_user_stats()
    # 5. Rendi template 'dashboard.html' con tasks, stats, filtro corrente
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 10: ROUTE CREA TASK (PROTETTA)
# =============================================================================


@app.route("/task/new", methods=["GET", "POST"])
# @login_required  # <-- DECOMMENTA
def new_task(current_user=None):
    """Crea nuovo task."""
    # TODO 10a:
    # GET: mostra template 'new_task.html'
    # POST:
    #   1. Ottieni title e description da request.form
    #   2. Valida: title non vuoto
    #   3. Crea task con create_task()
    #   4. Flash messaggio successo
    #   5. Redirect a dashboard
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 11: ROUTE MODIFICA TASK (PROTETTA)
# =============================================================================


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
# @login_required  # <-- DECOMMENTA
def edit_task(task_id, current_user=None):
    """Modifica task esistente."""
    # TODO 11a:
    # 1. Ottieni task con get_task_by_id()
    # 2. Se non esiste, flash errore e redirect a dashboard
    # GET: mostra template 'edit_task.html' con task
    # POST:
    #   1. Ottieni title e description da request.form
    #   2. Aggiorna con update_task()
    #   3. Flash messaggio
    #   4. Redirect a dashboard
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 12: ROUTE TOGGLE COMPLETATO (PROTETTA)
# =============================================================================


@app.route("/task/<int:task_id>/toggle", methods=["POST"])
# @login_required  # <-- DECOMMENTA
def toggle_task(task_id, current_user=None):
    """Segna task come completato/da fare."""
    # TODO 12a:
    # 1. Ottieni task con get_task_by_id()
    # 2. Se esiste, inverti valore di completed
    # 3. Aggiorna con update_task()
    # 4. Flash messaggio
    # 5. Redirect a dashboard
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 13: ROUTE ELIMINA TASK (PROTETTA)
# =============================================================================


@app.route("/task/<int:task_id>/delete", methods=["POST"])
# @login_required  # <-- DECOMMENTA
def delete_task_route(task_id, current_user=None):
    """Elimina un task."""
    # TODO 13a:
    # 1. Elimina con delete_task()
    # 2. Flash messaggio appropriato
    # 3. Redirect a dashboard
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# TODO 14: ROUTE STATISTICHE (PROTETTA)
# =============================================================================


@app.route("/stats")
# @login_required  # <-- DECOMMENTA
def stats(current_user=None):
    """Pagina statistiche dettagliate."""
    # TODO 14a:
    # 1. Ottieni tutti i task dell'utente
    # 2. Calcola statistiche avanzate:
    #    - Task per giorno della settimana
    #    - Task completati oggi
    #    - Task più vecchio non completato
    # 3. Rendi template 'stats.html' con dati
    pass  # <-- IMPLEMENTA QUI


# =============================================================================
# AVVIO APPLICAZIONE
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("📋 ESERCIZIO: TASK MANAGER CON BEARER TOKEN")
    print("=" * 70)
    print("\n🎯 TODO da completare:")
    print("   1. Configurazione (SECRET_KEY, TOKEN_EXPIRATION)")
    print("   2. Database simulato (USERS, ACTIVE_TOKENS, TASKS)")
    print("   3. Funzioni helper token (generate, create, verify)")
    print("   4. Decorator @login_required")
    print("   5. Funzioni helper task (get, create, update, delete, stats)")
    print("   6. Route /register")
    print("   7. Route /login")
    print("   8. Route /logout")
    print("   9. Route /dashboard")
    print("   10. Route /task/new")
    print("   11. Route /task/<id>/edit")
    print("   12. Route /task/<id>/toggle")
    print("   13. Route /task/<id>/delete")
    print("   14. Route /stats")
    print("\n🌐 Una volta completato, vai su http://localhost:5000")
    print("\n📝 Funzionalità da implementare:")
    print("   ✓ Registrazione utenti")
    print("   ✓ Login/Logout con Bearer Token")
    print("   ✓ Crea task personali")
    print("   ✓ Modifica task")
    print("   ✓ Segna come completato")
    print("   ✓ Elimina task")
    print("   ✓ Filtra task (tutti/completati/da fare)")
    print("   ✓ Visualizza statistiche")
    print("\n" + "=" * 70 + "\n")

    app.run(debug=True, port=5000)
