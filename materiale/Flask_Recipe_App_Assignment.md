# Consegna: Flask Recipe App con Login e Docker

## Obiettivo

Realizza una mini web app Flask per la gestione di ricette, con autenticazione tramite Bearer Token (opzionale: JWT). L'app deve permettere agli utenti di registrarsi, autenticarsi e caricare le proprie ricette, che devono includere:

-   Titolo
-   Descrizione
-   Ingredienti
-   Procedimento

L'applicazione deve utilizzare un database PostgreSQL e deve essere completamente dockerizzata. Bonus: aggiungi i test automatici e includili nella dockerizzazione.

---

## Requisiti

### 1. Backend Flask

-   **Autenticazione**: Implementa login tramite Bearer Token (puoi usare JWT come bonus).
-   **Modello Utente**: Gli utenti devono potersi registrare e autenticare.
-   **Modello Ricetta**: Ogni ricetta deve essere associata a un utente e contenere titolo, descrizione, ingredienti e procedimento.
-   **API**: Esporre endpoint REST per:
    -   Registrazione utente
    -   Login utente (restituisce token)
    -   Creazione ricetta (protetto da token)
    -   Visualizzazione ricette (pubblico o protetto, a scelta)

### 2. Frontend (facoltativo)

-   Puoi generare una semplice interfaccia HTML (anche generata con AI) per interagire con le API.

### 3. Database

-   Usa PostgreSQL come database principale.
-   Fornisci uno script o istruzioni per la creazione del database e delle tabelle.

### 4. Docker

-   Crea un `Dockerfile` per l'app Flask.
-   Crea un `docker-compose.yml` per avviare sia l'app che il database PostgreSQL.
-   Assicurati che l'app sia configurata per connettersi al database tramite variabili d'ambiente.

### 5. Bonus: Test

-   Scrivi test automatici (ad esempio con `pytest` o `unittest`).
-   Includi l'esecuzione dei test nel processo di build o come servizio separato in Docker Compose.

---

## Suggerimenti

-   Puoi usare librerie come `Flask-JWT-Extended` o `PyJWT` per la gestione dei token.
-   Per l'ORM puoi usare `SQLAlchemy`.
-   Per la gestione delle password usa `werkzeug.security`.
-   Ricorda di non committare mai le chiavi segrete o le password in chiaro.
-   Usa variabili d'ambiente per la configurazione.

---

## Consegna

-   Repository con codice, Dockerfile, docker-compose.yml e README con istruzioni per l'avvio.
-   Esempi di richieste API (puoi includere file Postman o curl).
-   (Bonus) Test automatici integrati nella pipeline Docker.

---

## Esempio di struttura cartella

```
Flask_Recipe_App/
├── app.py
├── models.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── tests/
│   └── test_api.py
└── ...
```

---

## Buon lavoro!
