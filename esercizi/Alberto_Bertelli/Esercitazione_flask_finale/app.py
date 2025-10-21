from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    flash,
)
from functools import wraps
import secrets
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, ValidationError
import re

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(16)  

TOKEN_EXPIRATION = timedelta(minutes=15)
ACTIVE_TOKENS={
    "demo_token_123": {
        "username": "alice",
        "expires": datetime.now() + timedelta(minutes=15),
        "created": datetime.now(),
    }
}
USERS={
    "alice": "password123",
    "bob": "mypass456",
    "carlo": "ricetta789"
}
RECIPES={
    "alice": [
        {
            "title": "Pasta al Pesto",
            "description": "Un classico piatto ligure con basilico fresco.",
            "ingredients": "Pasta, basilico, pinoli, olio, aglio, formaggio",
            "steps": "Cuoci la pasta, prepara il pesto, mescola e servi.",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    ],
    "bob": [
        {
            "title": "Tiramisù",
            "description": "Dolce al cucchiaio con mascarpone e caffè.",
            "ingredients": "Mascarpone, savoiardi, caffè, uova, cacao",
            "steps": "Monta le uova, aggiungi il mascarpone, alterna con savoiardi.",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    ],
    "carlo": []
}
#Generazione token
def generate_token():
    return secrets.token_urlsafe(32)

#Create token
def create_token(username):
    """Crea un nuovo token per l'utente."""
    token =generate_token()
    ACTIVE_TOKENS[token]={
        "username": username,
        "expires" : datetime.now() + TOKEN_EXPIRATION,
        "created" : datetime.now()
    }
    return token

#Verifica token
def verify_token(token):
    """Verifica se un token è valido e non scaduto."""
    if token not in ACTIVE_TOKENS:
        return None
    token_data = ACTIVE_TOKENS[token]
    #Facciamo la verifica se il token è scaduto
    if datetime.now()> token_data["expires"]:
        del ACTIVE_TOKENS[token]
        return None
    return token_data["username"]

def login_required(f):
    """Decorator per proteggere le pagine web."""

    @wraps(f)
    def decorated(*args, **kwargs):
        # Controlliamo se c'è un token nella session
        if "token" not in session:
            flash("effettuare il login per accedere alla pagina","error")
            return redirect(url_for("login"))
        
        userName = verify_token(session.get("token"))
        if not userName :
            flash("Token scaduto effettua di nuovo il login","error")
            session.pop("token",None)
            return redirect(url_for("login"))
        return f(current_user=userName, *args, **kwargs)
    return decorated

def api_token_required(f):
    """Decorator per proteggere gli endpoint API."""

    @wraps(f)
    def decorated(*args, **kwargs):
        # Ottengo token dalla session
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return (
                    jsonify(
                        {
                            "error": "Token malformato",
                            "message": "Usa il formato: Authorization: Bearer <token>",
                        }
                    ),
                    401,
                )
        if not token:
            return(
                jsonify(
                    {
                       "error": "Token mancante",
                        "message": "Effettua il login per ottenere un token", 
                    }
                ),
                401,
            )
        username = verify_token(token)
        if not username:
            return (
                jsonify(
                    {
                        "error": "Token non valido o scaduto",
                        "message": "Effettua nuovamente il login",
                    }
                ),
                401,
            )

        # Passa l'username alla funzione
        return f(current_user=username, *args, **kwargs)

    return decorated




@app.route("/")
def home():
    """Homepage - mostra se l'utente è loggato o meno."""
    is_logged_in = "token" in session and verify_token(session["token"]) is not None
    current_user = None

    if is_logged_in:
        current_user = verify_token(session["token"])

    return render_template(
        "index.html", is_logged_in=is_logged_in, current_user=current_user
    )

class RegisterForm(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)
    password: str = Field(...,min_length=8,max_length=50)
    confirm_password :str = Field(...,min_length=8,max_length=50)

@app.route  ("/register", methods=["GET","POST"])
def register():
    if request.method =="POST":
        errors = []
        try:
            form_data=RegisterForm.model_validate(request.form)
        except ValidationError as e:
            errors.append(f"errore di validazione: {e}")
        except Exception as e:
            errors.append(f"errore generico: {e}")

        if form_data.username in USERS:
            errors.append("Username già esistente")
        
        if not re.search(r'[A-Z]', form_data.password):
            errors.append("La password deve contenere almeno un carattere maiuscolo")
        if not re.search(r'[0-9]', form_data.password):
            errors.append("La password deve contenere almeno un carattere numerico")
        if not form_data.confirm_password == form_data.password:
            errors.append("La password è diversa dal confirm_password")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("register.html", form=request.form)
                            
        USERS[form_data.username] = {
            "password": form_data.password,
            "name": form_data.name,
            "role": form_data.role
            }
        return redirect(url_for("login"))
    return render_template("register.html")

class LoginForm(BaseModel) :
    username: str = Field(...,min_length=3,max_length=20)
    password: str = Field(...,min_length=8,max_length=50)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login - form HTML."""
    if request.method == "POST":
        login_data = LoginForm.model_validate(request.form)
        if login_data.username in USERS :
            if USERS[login_data.username]==login_data.password:
                flash("Sei loggato","success")
                token = create_token(login_data.username)
                session["token"]= token
                return redirect(url_for("dashboard"))
            else:
                flash("Credenziali non valide","error")
                return render_template("login.html", is_logged_in=False)
        else:
            flash("Credenziali non valide","error")
            return render_template("login.html", is_logged_in=False)
    return render_template("login.html", is_logged_in=False)


#logout per l'utente
@app.route("/logout")
def logout():
    """Logout - invalida token e cancella session."""
    # 1. Ottieni token da session
    token=session.get("token")
    # 2. Se esiste, rimuovilo da ACTIVE_TOKENS
    if token in ACTIVE_TOKENS:
        # 3. Rimuovi token dalla session
        del ACTIVE_TOKENS["token"]
        session.pop("token",None)
        # 4. Flash messaggio di successo
        flash("logout effettuato con successo","success")
    # 5. Redirect a home
    return redirect(url_for("login"))

#La parte della ricetta
class RecipesForm(BaseModel) :
    titolo: str = Field(...,min_length=3,max_length=20)
    descrizione: str = Field(...,min_length=20,max_length=50)
    ingredienti: str = Field(...,min_length=20,max_length=50)
    procedimento: str = Field(...,min_length=10,max_length=500)

@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard(current_user):
    #andiamo a vedere in base all'utente le ricette che ha
    user_recipes= RECIPES.get(current_user,[])
    if request.method == "POST":
        try:
            recipe_data= RecipesForm.model_validate(request.form)
        except ValidationError as e:
            flash(str(e), "error")
            return render_template(
                "dashboard.html", recipes=user_recipes, current_user=current_user
            )
        #qui creiamo una nuova ricetta
        new_recipe ={
            "titolo": recipe_data.titolo,
            "descrizione": recipe_data.descrizione,
            "ingredienti": recipe_data.ingredienti,
            "procedimento": recipe_data.procedimento,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        RECIPES.setdefault(current_user,[]).append(new_recipe)
        flash("Ricetta creata","success")
        return redirect(url_for("dashboard"))
    return render_template(
        "dashboard.html", recipes=user_recipes, current_user=current_user
    )

@app.route("/api/recipes", methods=["GET"])
@api_token_required
def api_get_recipes(current_user):
    return jsonify({"recipes": RECIPES.get(current_user, [])}), 200

if __name__ == "__main__":
    app.run(debug=True)