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
BASE_URL = os.environ.get("APP_BASE_URL", "http://127.0.0.1:5001/")

# Type alias per definire una funzione di check che prende una Session
CheckFn = Callable[[requests.Session], None]

def base_path(path: str) -> str:
    """Costruisce un URL completo dato un percorso relativo."""
    # Rimuove lo slash iniziale e unisce con BASE_URL
    return urljoin(BASE_URL, path.lstrip("/"))


def _check_protected(session: requests.Session) -> None:
    """Verifica che la homepage risponda correttamente."""
    # Effettua GET sulla root
    response = session.get(base_path("/login"), timeout=5)
    # Verifica che il codice di stato sia 200 (OK)
    if response.status_code == 401:
        raise AssertionError("GET / Corretto, non hai il permesso")


def _run_checks(checks: Iterable[tuple[str, CheckFn]]) -> int:
    """Esegue una serie di check e ritorna il codice di uscita."""
    # Crea una sessione HTTP per mantenere i cookie tra le richieste
    session = requests.Session()

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
        ("GET /", _check_protected),
    )
    # Esegue i check e ritorna il risultato
    return _run_checks(checks)


# Se il file è eseguito direttamente (non importato)
if __name__ == "__main__":
    # Esegue main() e usa il suo valore come exit code del programma
    sys.exit(main())
