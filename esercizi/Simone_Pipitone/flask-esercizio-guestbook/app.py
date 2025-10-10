# Importazione dal modulo __future__ per compatibilità con versioni precedenti di Python
from __future__ import annotations

# Importazione delle funzionalità principali di Flask
from flask import (
    Flask,  # Classe principale per creare l'applicazione web
    request,  # Oggetto per accedere ai dati delle richieste HTTP
    redirect,  # Funzione per reindirizzare l'utente ad un'altra pagina
    url_for,  # Funzione per generare URL basati sui nomi delle rotte
    render_template,  # Funzione per renderizzare i template HTML
    flash,  # Funzione per mostrare messaggi temporanei all'utente
    abort,  # Funzione per interrompere la richiesta con un errore HTTP
    jsonify,  # Funzione per convertire dati Python in formato JSON
    session,  # Dizionario per memorizzare dati persistenti per ogni utente
)

# Importazione di Path per gestire i percorsi dei file in modo sicuro
from pathlib import Path

# Importazione del modulo json per leggere/scrivere file JSON
import json

# Creazione dell'istanza dell'applicazione Flask
app = Flask(__name__)

# Chiave segreta necessaria per firmare i cookie di sessione e i messaggi flash
# NOTA: in produzione usare una chiave casuale e sicura, non "dev"!
app.secret_key = "dev"  # per demo: flash + session

# --- Storage (Gestione dello storage dei dati) ---

# Definizione della cartella dove salvare i dati
DATA_DIR = Path("data")

# Creazione della cartella se non esiste (exist_ok=True evita errori se già presente)
DATA_DIR.mkdir(exist_ok=True)

# Definizione del file JSON che conterrà tutti i messaggi
DATA_FILE = DATA_DIR / "messages.json"


# Funzione per caricare i messaggi dal file JSON
def load_messages():
    # Controlla se il file esiste
    if not DATA_FILE.exists():
        # Se non esiste, restituisce una lista vuota
        return []
    try:
        # Apre il file in modalità lettura con encoding UTF-8
        with DATA_FILE.open("r", encoding="utf-8") as f:
            # Carica e restituisce i dati JSON come lista Python
            return json.load(f)
    except json.JSONDecodeError:
        # Se il file è corrotto o non è un JSON valido, restituisce lista vuota
        return []


# Funzione per salvare i messaggi nel file JSON
def save_messages(messages):
    # Apre il file in modalità scrittura con encoding UTF-8
    with DATA_FILE.open("w", encoding="utf-8") as f:
        # Salva la lista come JSON formattato
        # ensure_ascii=False: permette caratteri accentati
        # indent=2: formatta il JSON con indentazione per leggibilità
        json.dump(messages, f, ensure_ascii=False, indent=2)


# Funzione per generare il prossimo ID disponibile per un nuovo messaggio
def next_id(messages):
    # Se ci sono messaggi, prende l'ID dell'ultimo e aggiunge 1
    # Altrimenti (lista vuota) restituisce 1 come primo ID
    return (messages[-1]["id"] + 1) if messages else 1


# --- Filtri Jinja (Funzioni personalizzate utilizzabili nei template) ---


# Decoratore per registrare un filtro personalizzato in Jinja2
@app.template_filter("truncate_italian")
def truncate_italian(s: str, n: int = 60) -> str:
    """Tronca una stringa a n caratteri, aggiungendo … se necessario"""
    # Se s è None o vuoto, usa stringa vuota
    s = s or ""
    # Se la stringa è più corta di n caratteri, restituiscila così com'è
    # Altrimenti taglia a n-1 caratteri e aggiungi il simbolo …
    return s if len(s) <= n else s[: max(0, n - 1)] + "…"


# --- Rotte (Route) ---


# Rotta principale: mostra la lista dei messaggi
@app.route("/")
def home():
    # Ottiene il parametro 'q' dalla query string per la ricerca (es: /?q=ciao)
    # strip() rimuove spazi, lower() converte in minuscolo
    q = (request.args.get("q") or "").strip().lower()

    # Ottiene il numero di pagina dalla query string (default: 1)
    # max(1, ...) assicura che sia almeno 1
    page = max(1, int(request.args.get("page", 1)))

    # Numero di messaggi per pagina
    per_page = 10

    # Carica tutti i messaggi dal file
    msgs = load_messages()

    # Ordina i messaggi per ID in ordine decrescente (più recenti prima)
    msgs = sorted(msgs, key=lambda m: m["id"], reverse=True)

    # Se c'è una query di ricerca
    if q:
        # Filtra i messaggi: mantiene solo quelli che contengono q nell'autore o nel testo
        msgs = [m for m in msgs if q in m["author"].lower() or q in m["text"].lower()]

    # Totale messaggi dopo il filtro
    total = len(msgs)

    # Calcola l'indice di inizio per la paginazione
    start = (page - 1) * per_page

    # Calcola l'indice di fine per la paginazione
    end = start + per_page

    # Estrae solo i messaggi per la pagina corrente
    page_items = msgs[start:end]

    # Extra: contatore visite (incrementa il contatore nella sessione)
    session["visits"] = session.get("visits", 0) + 1

    # Renderizza il template home.html passando tutte le variabili necessarie
    return render_template(
        "home.html",
        messages=page_items,  # Messaggi da visualizzare
        page=page,  # Numero pagina corrente
        per_page=per_page,  # Messaggi per pagina
        total=total,  # Totale messaggi
        q=q,  # Query di ricerca
        visits=session["visits"],  # Numero di visite dell'utente
    )


# Rotta per creare un nuovo messaggio (GET mostra il form, POST lo processa)
@app.route("/new", methods=["GET", "POST"])
def new_message():
    # Se la richiesta è POST (invio del form)
    if request.method == "POST":
        # Ottiene l'autore dal form, rimuovendo spazi
        author = (request.form.get("author") or "").strip()

        # Ottiene il testo dal form, rimuovendo spazi
        text = (request.form.get("text") or "").strip()

        # Lista per raccogliere eventuali errori di validazione
        errors = []

        # Validazione: l'autore è obbligatorio
        if not author:
            errors.append("Author obbligatorio.")

        # Validazione: il testo è obbligatorio
        if not text:
            errors.append("Text obbligatorio.")

        # Validazione: l'autore non può superare 30 caratteri
        if len(author) > 30:
            errors.append("Author troppo lungo (max 30).")

        # Validazione: il testo non può superare 200 caratteri
        if len(text) > 200:
            errors.append("Text troppo lungo (max 200).")

        # Se ci sono errori di validazione
        if errors:
            # Per ogni errore, aggiungilo ai messaggi flash
            for e in errors:
                flash(e)

            # Renderizza nuovamente il form con i dati inseriti e status HTTP 400 (Bad Request)
            return render_template("new.html", author=author, text=text), 400

        # Carica tutti i messaggi esistenti
        msgs = load_messages()

        # Genera un nuovo ID per il messaggio
        mid = next_id(msgs)

        # Aggiunge il nuovo messaggio alla lista
        msgs.append({"id": mid, "author": author, "text": text})

        # Salva la lista aggiornata nel file
        save_messages(msgs)

        # Reindirizza alla homepage dopo il salvataggio
        return redirect(url_for("home"))

    # Se la richiesta è GET, mostra il form vuoto
    return render_template("new.html")


# Rotta per visualizzare un singolo messaggio in dettaglio
@app.route("/msg/<int:msg_id>")
def show_message(msg_id: int):
    # Carica tutti i messaggi
    msgs = load_messages()

    # Cerca il messaggio con l'ID specificato
    # next() restituisce il primo elemento che soddisfa la condizione, o None se non trovato
    m = next((m for m in msgs if m["id"] == msg_id), None)

    # Se il messaggio non è stato trovato
    if not m:
        # Restituisce errore 404 (Not Found)
        abort(404)

    # Renderizza il template show.html passando il messaggio trovato
    return render_template("show.html", m=m)


# Extra opzionale: rotta per esportare tutti i messaggi in formato JSON
@app.route("/export.json")
def export_json():
    # Restituisce tutti i messaggi come risposta JSON
    return jsonify(load_messages())


# Gestore personalizzato per l'errore 404 (pagina non trovata)
@app.errorhandler(404)
def not_found(e):
    # Renderizza il template 404.html con status code 404
    return render_template("404.html"), 404
