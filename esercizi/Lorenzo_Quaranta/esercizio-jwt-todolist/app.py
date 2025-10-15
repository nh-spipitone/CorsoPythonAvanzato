"""
Esercizio: Todo List con JWT Authentication

TODO List:
1. [ ] Importare le librerie necessarie (Flask, jwt, werkzeug.security, datetime, functools)
2. [ ] Configurare l'app Flask e la SECRET_KEY
3. [ ] Implementare le funzioni helper per leggere/scrivere db.json
4. [ ] Implementare la route POST /register per registrare nuovi utenti
5. [ ] Implementare la route POST /login per autenticare e generare JWT
6. [ ] Creare il decorator @token_required per proteggere le route
7. [ ] Implementare GET /api/todos per ottenere i todo dell'utente
8. [ ] Implementare POST /api/todos per creare un nuovo todo
9. [ ] Implementare PUT /api/todos/<id> per modificare un todo
10. [ ] Implementare DELETE /api/todos/<id> per eliminare un todo
11. [ ] Creare le route per le pagine HTML (home, register, login, todos)
12. [ ] Testare l'applicazione

HINT: Struttura base
"""

from flask import Flask, request, jsonify, render_template
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# TODO 2: Configurare la SECRET_KEY
# HINT: app.config['SECRET_KEY'] = 'la-tua-chiave-segreta-super-sicura'
app.config["SECRET_KEY"] = "your-secret-key-change-this-in-production"

DB_FILE = "db.json"

# =============================================
# HELPER FUNCTIONS
# =============================================


def load_db():
    """
    TODO 3a: Implementare la funzione per caricare il database JSON

    HINT:
    - Controllare se il file esiste
    - Se esiste, aprirlo e caricare il JSON
    - Se non esiste, restituire un dizionario con users=[] e todos=[]
    """
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": [], "todos": []}


def save_db(data):
    """
    TODO 3b: Implementare la funzione per salvare il database JSON

    HINT:
    - Aprire il file in modalità scrittura
    - Usare json.dump con indent=2 per formattazione leggibile
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_id(items):
    """
    Helper per ottenere il prossimo ID disponibile
    """
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


# =============================================
# DECORATOR PER AUTENTICAZIONE
# =============================================


def token_required(f):
    """
    TODO 6: Implementare il decorator per verificare il JWT token

    HINT:
    - Usare @wraps(f) per preservare i metadati della funzione
    - Leggere l'header 'Authorization' dalla request
    - Il formato è "Bearer <token>"
    - Estrarre il token dopo "Bearer "
    - Decodificare il token con jwt.decode()
    - In caso di errore o token mancante, restituire errore 401
    - Passare i dati dell'utente corrente alla funzione decorata

    Esempio:
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Estrarre il token

        if not token:
            return jsonify({'message': 'Token mancante!'}), 401

        try:
            # Decodificare il token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Recuperare l'utente dal database
            db = load_db()
            current_user = None
            for user in db['users']:
                if user['id'] == data['user_id']:
                    current_user = user
                    break

            if not current_user:
                return jsonify({'message': 'Utente non trovato!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token scaduto!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token non valido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # TODO: Implementare la logica del decorator
        token = None

        # Leggere l'header Authorization
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]  # Formato: "Bearer <token>"
            except IndexError:
                return jsonify({"message": "Formato token non valido!"}), 401

        if not token:
            return jsonify({"message": "Token mancante!"}), 401

        try:
            # Decodificare il token
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

            # Recuperare l'utente
            db = load_db()
            current_user = None
            for user in db["users"]:
                if user["id"] == data["user_id"]:
                    current_user = user
                    break

            if not current_user:
                return jsonify({"message": "Utente non trovato!"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token scaduto!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token non valido!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# =============================================
# ROUTES - AUTENTICAZIONE
# =============================================


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    TODO 4: Implementare la registrazione utente

    GET: Restituire il template register.html
    POST:
    - Leggere username e password dal JSON body
    - Verificare che l'username non esista già
    - Hashare la password con generate_password_hash()
    - Salvare il nuovo utente nel database
    - Restituire successo o errore

    HINT per hashing:
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    """
    if request.method == "GET":
        return render_template("register.html")

    # TODO: Implementare la logica POST
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username e password richiesti!"}), 400

    username = data["username"]
    password = data["password"]

    # Caricare database
    db = load_db()

    # Verificare se l'utente esiste già
    for user in db["users"]:
        if user["username"] == username:
            return jsonify({"message": "Username già esistente!"}), 409

    # Creare nuovo utente
    new_user = {
        "id": get_next_id(db["users"]),
        "username": username,
        "password": generate_password_hash(password, method="pbkdf2:sha256"),
    }

    db["users"].append(new_user)
    save_db(db)

    return jsonify({"message": "Utente registrato con successo!"}), 201


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    TODO 5: Implementare il login e generazione JWT

    GET: Restituire il template login.html
    POST:
    - Leggere username e password dal JSON body
    - Trovare l'utente nel database
    - Verificare la password con check_password_hash()
    - Generare un JWT token con scadenza 24h
    - Restituire il token

    HINT per JWT:
    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    """
    if request.method == "GET":
        return render_template("login.html")

    # TODO: Implementare la logica POST
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username e password richiesti!"}), 400

    username = data["username"]
    password = data["password"]

    # Caricare database e trovare l'utente
    db = load_db()
    user = None
    for u in db["users"]:
        if u["username"] == username:
            user = u
            break

    if not user:
        return jsonify({"message": "Credenziali non valide!"}), 401

    # Verificare la password
    if not check_password_hash(user["password"], password):
        return jsonify({"message": "Credenziali non valide!"}), 401

    # Generare JWT token
    token = jwt.encode(
        {
            "user_id": user["id"],
            "username": user["username"],
            "exp": datetime.utcnow() + timedelta(hours=24),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return jsonify({"token": token}), 200


# =============================================
# ROUTES - TODO API (PROTETTE)
# =============================================


@app.route("/api/todos", methods=["GET"])
@token_required
def get_todos(current_user):
    """
    TODO 7: Implementare GET dei todo dell'utente corrente

    HINT:
    - Caricare il database
    - Filtrare i todo per user_id == current_user['id']
    - Restituire la lista in JSON
    """
    db = load_db()
    user_todos = [todo for todo in db["todos"] if todo["user_id"] == current_user["id"]]
    return jsonify({"todos": user_todos}), 200


@app.route("/api/todos", methods=["POST"])
@token_required
def create_todo(current_user):
    """
    TODO 8: Implementare POST per creare un nuovo todo

    HINT:
    - Leggere title, description dal JSON body
    - Creare un nuovo todo con:
      - id: next_id
      - user_id: current_user['id']
      - title, description
      - completed: False
      - created_at: timestamp corrente
    - Salvare nel database
    """
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"message": "Il campo title è richiesto!"}), 400

    db = load_db()

    new_todo = {
        "id": get_next_id(db["todos"]),
        "user_id": current_user["id"],
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }

    db["todos"].append(new_todo)
    save_db(db)

    return jsonify({"message": "Todo creato!", "todo": new_todo}), 201


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
@token_required
def update_todo(current_user, todo_id):
    """
    TODO 9: Implementare PUT per modificare un todo

    HINT:
    - Trovare il todo per ID
    - Verificare che appartenga all'utente corrente
    - Aggiornare i campi (title, description, completed)
    - Salvare nel database
    """
    data = request.get_json()
    db = load_db()

    # Trovare il todo
    todo = None
    for t in db["todos"]:
        if t["id"] == todo_id:
            todo = t
            break

    if not todo:
        return jsonify({"message": "Todo non trovato!"}), 404

    # Verificare ownership
    if todo["user_id"] != current_user["id"]:
        return jsonify({"message": "Non autorizzato!"}), 403

    # Aggiornare i campi
    if "title" in data:
        todo["title"] = data["title"]
    if "description" in data:
        todo["description"] = data["description"]
    if "completed" in data:
        todo["completed"] = data["completed"]

    save_db(db)

    return jsonify({"message": "Todo aggiornato!", "todo": todo}), 200


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
@token_required
def delete_todo(current_user, todo_id):
    """
    TODO 10: Implementare DELETE per eliminare un todo

    HINT:
    - Trovare il todo per ID
    - Verificare che appartenga all'utente corrente
    - Rimuoverlo dalla lista
    - Salvare nel database
    """
    db = load_db()

    # Trovare il todo
    todo = None
    for t in db["todos"]:
        if t["id"] == todo_id:
            todo = t
            break

    if not todo:
        return jsonify({"message": "Todo non trovato!"}), 404

    # Verificare ownership
    if todo["user_id"] != current_user["id"]:
        return jsonify({"message": "Non autorizzato!"}), 403

    # Rimuovere il todo
    db["todos"] = [t for t in db["todos"] if t["id"] != todo_id]
    save_db(db)

    return jsonify({"message": "Todo eliminato!"}), 200


# =============================================
# ROUTES - PAGINE HTML
# =============================================


@app.route("/")
def index():
    """
    TODO 11a: Homepage con informazioni sull'API
    """
    return render_template("index.html")


@app.route("/todos")
def todos_page():
    """
    TODO 11b: Pagina per gestire i todo (richiede autenticazione lato client)
    """
    return render_template("todos.html")


# =============================================
# MAIN
# =============================================

if __name__ == "__main__":
    app.run(debug=True)
