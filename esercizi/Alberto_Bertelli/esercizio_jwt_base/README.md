# Esercizio: JWT Authentication Basics

Obiettivo: implementare un mini servizio Flask che gestisca autenticazione tramite JSON Web Token (JWT).

## Requisiti

-   Python 3.10+
-   Flask
-   PyJWT (`pip install pyjwt`)

## Istruzioni

1. Apri `app.py` e completa i `TODO`:

-   Genera un token firmato al login con claim aggiuntivi (`role`, `email`, `is_premium`).
-   Verifica il token nelle rotte protette e passa il payload alla vista.
-   Crea il decoratore `premium_required` per limitare una rotta dedicata agli utenti premium.
-   Gestisci le note private dell'utente autenticato.

2. Avvia il server con `flask --app app.py --debug run`.
3. Usa strumenti come `curl` o Postman per testare gli endpoint.

### Endpoints richiesti

-   `POST /login` accetta `username` e `password` e restituisce un JWT valido 45 minuti.
-   `GET /protected` disponibile solo con header `Authorization: Bearer <token>`.
-   `GET /me` restituisce informazioni lette dal token già verificato e il tempo residuo.
-   `POST /notes` salva una nota privata per l'utente corrente.
-   `GET /notes/premium` restituisce tutte le note ma solo per chi possiede il claim `is_premium`.

### Suggerimenti

-   Usa `datetime.now(timezone.utc)` per gestire claim `iat` ed `exp`.
-   Ricordati di importare ciò che ti serve (es. `datetime`, `timezone`).
-   Nel decoratore `jwt_required` rilancia la vista passando `current_user=payload`.
-   Per il decoratore `premium_required` restituisci uno stato `403` quando il claim `is_premium` è falso.

### Test rapidi

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'

curl http://127.0.0.1:5000/protected \
  -H "Authorization: Bearer YOUR_JWT"

curl -X POST http://127.0.0.1:5000/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT" \
  -d '{"text":"Prima nota"}'
```

Buon lavoro!
