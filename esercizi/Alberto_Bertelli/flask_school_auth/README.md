# Esercizio Flask: Autenticazione Registro Scolastico 🔐

Un esercizio pratico per implementare un sistema di autenticazione completo utilizzando Flask-Login su un'applicazione di registro scolastico già funzionante.

## 📖 Descrizione

Questo progetto è un **esercizio guidato** dove dovrai implementare solo la parte di autenticazione. L'applicazione del registro scolastico (gestione studenti, voti e presenze) è già completa e funzionante.

Il tuo compito è aggiungere:

-   Sistema di login/logout
-   Protezione delle route sensibili
-   User session management
-   Flash messages per feedback utente

## 🎯 Obiettivi di Apprendimento

Dopo aver completato questo esercizio, saprai:

-   ✅ Come configurare Flask-Login
-   ✅ Come implementare una classe User con UserMixin
-   ✅ Come gestire l'autenticazione degli utenti
-   ✅ Come proteggere route con `@login_required`
-   ✅ Come gestire sessioni utente
-   ✅ Come utilizzare `current_user`
-   ✅ Come hashare e verificare password con Werkzeug

## 🚀 Setup Rapido

1. **Installa le dipendenze:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Avvia l'applicazione:**

    ```bash
    python app.py
    ```

3. **Apri il browser:**
    ```
    http://127.0.0.1:5000
    ```

## 🔑 Credenziali di Test

-   **Professore**: `prof.rossi` / `prof123`
-   **Segreteria**: `segreteria` / `segreteria123`

## 📋 Task da Completare

Cerca nel file `app.py` i commenti `TODO` e completa il codice:

### ✅ TODO 1: Configurazione Flask-Login

Inizializza LoginManager e configura le impostazioni base.

### ✅ TODO 2: Classe User

Implementa la classe User che eredita da UserMixin.

### ✅ TODO 3: User Loader

Implementa la funzione per caricare gli utenti dal database.

### ✅ TODO 4: Route di Login

Gestisci la logica di autenticazione nel POST della route login.

### ✅ TODO 5: Route di Logout

Implementa la funzionalità di logout.

### ✅ TODO 6: Protezione Route

Proteggi le route sensibili con il decoratore `@login_required`.

## 📚 Struttura del Progetto

```
flask_school_auth/
├── app.py                      # File principale (DA COMPLETARE)
├── requirements.txt            # Dipendenze Python
├── CONSEGNA.md                # Istruzioni dettagliate
├── README.md                  # Questo file
├── db.json                    # Database JSON (già popolato)
├── static/
│   └── style.css             # Stili CSS (già completo)
└── templates/
    ├── base.html             # Template base (già completo)
    ├── index.html            # Homepage (già completo)
    ├── login.html            # Pagina login (già completo)
    ├── dashboard.html        # Dashboard (già completo)
    ├── students.html         # Lista studenti (già completo)
    ├── student_detail.html   # Dettaglio studente (già completo)
    ├── form_grade.html       # Form voto (già completo)
    └── form_attendance.html  # Form presenza (già completo)
```

## ✅ Come Verificare il Tuo Lavoro

### Test 1: Login con Credenziali Errate

```
1. Vai su /login
2. Inserisci credenziali errate
3. ✅ Deve mostrare un messaggio di errore
```

### Test 2: Login Corretto

```
1. Vai su /login
2. Usa: prof.rossi / prof123
3. ✅ Deve reindirizzare a /dashboard
4. ✅ Deve mostrare il nome utente nella navbar
```

### Test 3: Protezione Route

```
1. Logout se sei loggato
2. Prova ad accedere a /students
3. ✅ Deve reindirizzare a /login
4. ✅ Deve mostrare un messaggio
```

### Test 4: Navigazione Completa

```
1. Login → Dashboard → Studenti
2. Clicca su un studente
3. Aggiungi un voto
4. Aggiungi una presenza
5. Logout
6. ✅ Tutto deve funzionare correttamente
```

## 🎓 Concetti Chiave

### Flask-Login

```python
from flask_login import (
    LoginManager,        # Gestisce le sessioni
    UserMixin,          # Classe base per User
    login_user,         # Fa il login
    logout_user,        # Fa il logout
    login_required,     # Protegge le route
    current_user        # Utente corrente
)
```

### Password Hashing

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Genera hash
hashed = generate_password_hash("password123")

# Verifica password
is_valid = check_password_hash(hashed, "password123")
```

## 🏆 Bonus Challenge

Se finisci in anticipo, prova a:

1. **Registrazione Utenti**: Aggiungi una route `/register`
2. **Remember Me**: Implementa l'opzione "Ricordami"
3. **Ruoli Utente**: Aggiungi ruoli (admin, prof, studente)
4. **Profilo Utente**: Crea una pagina profilo
5. **Change Password**: Permetti di cambiare password

## ⚠️ Note Importanti

-   ⛔ **NON modificare** le funzioni del registro scolastico
-   ⛔ **NON modificare** i template HTML
-   ⛔ **NON modificare** il file CSS
-   ✅ Concentrati **SOLO** sull'autenticazione
-   ✅ Segui i commenti TODO nel codice

## 🐛 Troubleshooting

### Errore: ModuleNotFoundError: No module named 'flask_login'

```bash
pip install flask-login
```

### Errore: working outside of application context

Assicurati di aver configurato correttamente il LoginManager con `init_app(app)`

### Le route protette non reindirizzano a login

Verifica di aver impostato `login_manager.login_view = "login"`

## 📖 Risorse Utili

-   [Flask-Login Documentation](https://flask-login.readthedocs.io/)
-   [Flask Documentation](https://flask.palletsprojects.com/)
-   [Werkzeug Security](https://werkzeug.palletsprojects.com/en/latest/utils/#module-werkzeug.security)

## 📤 Consegna

1. ✅ Completa tutti i TODO nel file `app.py`
2. ✅ Testa tutte le funzionalità
3. ✅ Verifica che non ci siano errori
4. ✅ (Opzionale) Committa su GitHub

## 👨‍🏫 Per i Docenti

Questo esercizio è stato progettato per:

-   Tempo stimato: 1-2 ore
-   Livello: Intermedio
-   Prerequisiti: Conoscenza base di Flask
-   Obiettivo: Implementazione pratica di autenticazione

---

**Buon lavoro! 💪**

Se hai domande, chiedi pure al docente!
