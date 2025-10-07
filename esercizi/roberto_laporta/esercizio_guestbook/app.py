from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev"

# Lascio almeno due esempi per testare subito il funzionamento della home
messages = [
    {
        "id": 1,
        "author": "Roberto",
        "text": "testo_fake",
    },
    {
        "id": 2,
        "author": "Jhon",
        "text": "testo_fake_secondo",
    }
]

# Generazione di ID (normalmente dovrebbe essere gestito da DB, quindi vado hardcoded)
def create_dynamic_id():
    len(messages) + 1

# home che mostra la lista dei messaggi
@app.get("/")
def get_messages():
    return render_template(
        "home.html", 
        messages=messages      
    )

# rimanda al form di creazione messaggio
@app.get('/new')
def new_message(): 
    return render_template("form.html")
    
# questo serve a completare la creazione messaggio
# IMPORTANTE - Ho inserito i controlli dei form nell'html, in modo da bloccare la scrittura se oltrepassati i caratteri
@app.post('/new')
def create_message():
    author = request.form.get(
        "author"
    )
    text = request.form.get(
        "text"
    )
  
    new_message = {
        "id": create_dynamic_id(),
        "author": author,
        "text": text,
    }
    messages.append(new_message)
    return redirect(url_for('get_messages')) 

# cerchiamo un messaggio tramite id
@app.get('/msg/<int:msg_id>')
def get_detail(msg_id: int):
    try:
        found_message = next(
            message for message in messages if message["id"] == msg_id
        )
        return render_template('message.html', message=found_message) 
    except:
        return f"Nessun messaggio con id {msg_id}", 404


app.run()