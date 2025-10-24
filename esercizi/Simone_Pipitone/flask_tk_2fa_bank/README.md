# Flask + Tkinter Authenticator (2FA) — Mini Banca

WebApp Flask con login + OTP (TOTP) e un **Authenticator** scritto in **Tkinter**.
DB: **PostgreSQL**. Funzioni: **saldo**, **deposito**, **prelievo**, **bonifico**.

## Avvio rapido con Docker (consigliato)

```bash
docker compose up --build
# Web: http://127.0.0.1:5000
```

Credenziali demo:
- Username: `student`
- Password: `password123`
- TOTP secret: `JBSWY3DPEHPK3PXP` (già configurato anche nel Tkinter)

## Avvio locale (senza Docker)
1. Avvia PostgreSQL e crea il DB `appdb` con utente `app`/`app` oppure modifica `DATABASE_URL` in `.env`.
2. Ambiente Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Win: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # personalizza se necessario
   ```
3. Lancia il server:
   ```bash
   flask --app app run --debug
   ```
   Web: http://127.0.0.1:5000

## Authenticator Tkinter
In un altro terminale:
```bash
python tk_authenticator/authenticator.py
```
Mostra il codice TOTP corrente per il secret demo. Copialo nella pagina OTP.

## Struttura
```
app/
  __init__.py
  models.py
  auth.py
  bank.py
  templates/
    base.html
    login.html
    otp.html
    dashboard.html
tk_authenticator/
  authenticator.py
requirements.txt
Dockerfile
docker-compose.yml
.env.example
```

## Nota didattica
Questo progetto è pensato per esercizio. In produzione servono: password più robuste, CSRF, rate limiting, logging, migrazioni DB e controlli aggiuntivi lato server.
