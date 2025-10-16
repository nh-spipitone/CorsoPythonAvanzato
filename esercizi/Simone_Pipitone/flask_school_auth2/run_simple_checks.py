"""Esegue semplici verifiche HTTP sull'app Flask in esecuzione."""

# Importazione per supportare le type annotations moderne
from __future__ import annotations

# Importazioni standard
import os  # Per accedere alle variabili d'ambiente
import sys  # Per gestire l'exit code del programma
import time  # Per implementare timeout e attese
from typing import Callable, Iterable  # Per le type hints
from urllib.parse import urljoin  # Per costruire URL completi

import requests  # Libreria per fare richieste HTTP

# URL base dell'app, leggibile da variabile d'ambiente o default locale
BASE_URL = os.environ.get("APP_BASE_URL", "http://127.0.0.1:5000/")
# Timeout massimo per attendere che il server sia pronto
TIMEOUT_SECONDS = float(os.environ.get("APP_CHECK_TIMEOUT", "10"))

# Type alias per definire una funzione di check che prende una Session
CheckFn = Callable[[requests.Session], None]


def _wait_for_server(session: requests.Session) -> bool:
    """Attende che il server Flask sia disponibile."""
    # Calcola il timestamp entro cui il server deve rispondere
    deadline = time.time() + TIMEOUT_SECONDS
    # Continua a provare finché non scade il timeout
    while time.time() < deadline:
        try:
            # Tenta di contattare l'URL base
            response = session.get(BASE_URL, timeout=2)
        except requests.RequestException:
            # Se c'è un errore di rete, attende e riprova
            time.sleep(0.5)
            continue
        # Se il server risponde con codice < 500, è pronto
        if response.status_code < 500:
            return True
        # Altrimenti attende e riprova
        time.sleep(0.5)
    # Se scade il timeout, ritorna False
    return False


def _check_home(session: requests.Session) -> None:
    """Verifica che la homepage risponda correttamente."""
    # Effettua GET sulla root
    response = session.get(base_path("/"), timeout=5)
    # Verifica che il codice di stato sia 200 (OK)
    if response.status_code != 200:
        raise AssertionError("GET / non ha restituito 200")
    # Verifica che la pagina contenga il testo atteso
    if "Registro Scolastico" not in response.text:
        raise AssertionError("La homepage non contiene il testo atteso")


def _check_dashboard_requires_login(session: requests.Session) -> None:
    """Verifica che /dashboard richieda autenticazione."""
    # Effettua GET senza seguire redirect automatici
    response = session.get(base_path("/dashboard"), allow_redirects=False, timeout=5)
    # Verifica che ci sia un redirect (302)
    if response.status_code != 302:
        raise AssertionError("/dashboard dovrebbe reindirizzare al login")
    # Ottiene l'URL di destinazione del redirect
    destination = response.headers.get("Location", "")
    # Verifica che il redirect porti a /login
    if "/login" not in destination:
        raise AssertionError("/dashboard non rimanda a /login")


def _check_login_flow(session: requests.Session) -> None:
    """Verifica che il login funzioni correttamente."""
    # Effettua POST con credenziali valide, seguendo i redirect
    response = session.post(
        base_path("/login"),
        data={"username": "prof.rossi", "password": "prof123"},
        allow_redirects=True,
        timeout=5,
    )
    # Verifica che la risposta finale sia 200
    if response.status_code != 200:
        raise AssertionError("Login non ha restituito 200")
    # Verifica che si sia raggiunta la dashboard
    if "Dashboard - Benvenuto" not in response.text:
        raise AssertionError("Login non ha raggiunto la dashboard")


def base_path(path: str) -> str:
    """Costruisce un URL completo dato un percorso relativo."""
    # Rimuove lo slash iniziale e unisce con BASE_URL
    return urljoin(BASE_URL, path.lstrip("/"))


def _run_checks(checks: Iterable[tuple[str, CheckFn]]) -> int:
    """Esegue una serie di check e ritorna il codice di uscita."""
    # Crea una sessione HTTP per mantenere i cookie tra le richieste
    session = requests.Session()
    # Attende che il server sia disponibile
    if not _wait_for_server(session):
        print("[check] impossibile contattare l'app in tempo utile")
        return 1  # Exit code 1 indica errore

    # Lista per tenere traccia dei check falliti
    failures = []
    # Itera su ogni check
    for name, func in checks:
        try:
            # Esegue la funzione di check
            func(session)
        except Exception as exc:  # Cattura qualsiasi eccezione
            # Stampa il fallimento
            print(f"[check] {name}: FAIL - {exc}")
            # Aggiunge alla lista dei fallimenti
            failures.append(name)
        else:
            # Se non ci sono eccezioni, il check è passato
            print(f"[check] {name}: OK")

    # Ritorna 1 se ci sono fallimenti, 0 altrimenti
    return 1 if failures else 0


def main() -> int:
    """Funzione principale che definisce ed esegue i check."""
    # Tuple di check da eseguire: (nome, funzione)
    checks = (
        ("GET /", _check_home),
        ("GET /dashboard", _check_dashboard_requires_login),
        ("POST /login", _check_login_flow),
    )
    # Esegue i check e ritorna il risultato
    return _run_checks(checks)


# Se il file è eseguito direttamente (non importato)
if __name__ == "__main__":
    # Esegue main() e usa il suo valore come exit code del programma
    sys.exit(main())
