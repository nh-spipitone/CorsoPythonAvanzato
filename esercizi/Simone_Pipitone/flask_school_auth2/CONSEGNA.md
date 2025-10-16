# Esercizio Flask: Sistema di Autenticazione per Registro Scolastico

## 📋 Obiettivo

Implementare un sistema di autenticazione completo per l'applicazione del Registro Scolastico utilizzando **Flask-Login**. L'applicazione gestionale è già completa: dovrai solo aggiungere il layer di autenticazione per proteggere le route.

## 🎯 Cosa Devi Fare

Devi completare le parti mancate nel file `app.py` per implementare:

1. **Configurazione Flask-Login**: Inizializzare il LoginManager
2. **Classe User**: Implementare la classe User che estende UserMixin
3. **User Loader**: Implementare la funzione per caricare gli utenti
4. **Route di Login**: Gestire login con validazione credenziali
5. **Route di Logout**: Implementare il logout
6. **Protezione Route**: Proteggere le route sensibili con `@login_required`

## 📦 Setup Iniziale

1. Crea un ambiente virtuale (se non l'hai già fatto):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

3. Avvia l'applicazione:

```bash
python app.py
```

## 🔑 Credenziali di Test

Nel database simulato sono già presenti questi utenti:

-   **Professore**:
    -   Username: `prof.rossi`
    -   Password: `prof123`
-   **Segreteria**:
    -   Username: `segreteria`
    -   Password: `segreteria123`

## 📝 Task da Completare

Cerca nel file `app.py` i seguenti commenti e completa il codice:

### 1️⃣ Configurazione Flask-Login

```python
# TODO 1: Inizializza Flask-Login
# - Crea un'istanza di LoginManager
# - Inizializzala con l'app Flask
# - Imposta login_view su "login"
# - Imposta un messaggio personalizzato per login_message
```

### 2️⃣ Classe User

```python
# TODO 2: Implementa la classe User
# - Deve ereditare da UserMixin
# - Deve avere un costruttore che accetta username
# - Deve impostare self.id con lo username
# - Deve impostare self.name dal database users_db
```

### 3️⃣ User Loader

```python
# TODO 3: Implementa la funzione user_loader
# - Usa il decoratore @login_manager.user_loader
# - Controlla se username esiste in users_db
# - Ritorna un oggetto User se esiste, None altrimenti
```

### 4️⃣ Route di Login

```python
# TODO 4: Implementa la logica di login POST
# - Recupera username e password dal form
# - Verifica se l'utente esiste nel database
# - Verifica la password con check_password_hash
# - Se corrette: login_user() e redirect a dashboard
# - Se errate: flash message di errore e resta su login
```

### 5️⃣ Route di Logout

```python
# TODO 5: Implementa la route di logout
# - Usa il decoratore @login_required
# - Chiama logout_user()
# - Redirect alla homepage
```

### 6️⃣ Protezione Route

```python
# TODO 6: Proteggi le seguenti route con @login_required
# - students_list
# - student_detail
# - new_grade
# - create_grade
# - new_attendance
# - create_attendance
```

## ✅ Come Verificare

1. **Test Login**:

    - Vai su `http://127.0.0.1:5000/login`
    - Prova a loggarti con credenziali errate → Deve mostrare errore
    - Loggati con `prof.rossi` / `prof123` → Deve portarti alla dashboard

2. **Test Protezione Route**:

    - Senza essere loggato, prova ad accedere a `/students`
    - Devi essere reindirizzato a `/login`

3. **Test Logout**:

    - Dopo aver fatto login, clicca su "Logout"
    - Devi essere reindirizzato alla homepage
    - Prova ad accedere a `/students` → Devi essere reindirizzato a login

4. **Test Navigazione Completa**:
    - Login → Dashboard → Lista Studenti → Dettaglio Studente
    - Aggiungi un voto
    - Aggiungi una presenza
    - Logout

## 🎓 Concetti da Studiare

Prima di iniziare, assicurati di conoscere:

-   **Flask-Login**: `LoginManager`, `UserMixin`, `login_user`, `logout_user`, `login_required`, `current_user`
-   **Werkzeug Security**: `generate_password_hash`, `check_password_hash`
-   **Flask Flash Messages**: Per mostrare feedback all'utente
-   **Decoratori Python**: Come funziona `@login_required`

## 📚 Risorse Utili

-   [Flask-Login Documentation](https://flask-login.readthedocs.io/)
-   [Werkzeug Security](https://werkzeug.palletsprojects.com/en/latest/utils/#module-werkzeug.security)
-   [Flask Flash Messages](https://flask.palletsprojects.com/en/latest/patterns/flashing/)

## 🏆 Bonus (Opzionale)

Se finisci in anticipo, prova a:

1. Aggiungere una route di registrazione per nuovi utenti
2. Implementare il parametro "Ricordami" nel login
3. Aggiungere ruoli utente (admin, professore, studente) con permessi diversi
4. Mostrare il nome dell'utente loggato nella navbar
5. Implementare un sistema di password dimenticata

## ⚠️ Note Importanti

-   **NON modificare** le funzionalità esistenti del registro scolastico
-   **NON modificare** i template HTML (sono già pronti)
-   Concentrati **SOLO** sull'implementazione dell'autenticazione
-   Il database `users_db` è già configurato, non modificarlo

## 📤 Consegna

Una volta completato l'esercizio:

1. Testa tutte le funzionalità
2. Assicurati che non ci siano errori
3. Verifica che tutte le route protette funzionino correttamente
4. (Opzionale) Committa il codice su GitHub

Buon lavoro! 💪
