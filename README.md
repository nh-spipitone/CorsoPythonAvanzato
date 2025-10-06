# Corso Python Avanzato

Repository per il corso di Python Avanzato contenente materiali didattici, esercizi e utilities.

## 📋 Descrizione

Questo repository contiene il materiale del corso di Python Avanzato, organizzato in moduli che coprono vari aspetti della programmazione Python avanzata, inclusi:

-   **Utilities**: Librerie di supporto per la sanificazione e normalizzazione del testo
-   **Esercizi**: Esercitazioni pratiche su Flask e altri argomenti
-   **Test**: Suite di test per validare le implementazioni

## 🚀 Setup

### Prerequisiti

-   Python >= 3.11
-   pip

### Installazione

1. **Clona la repository** (se non l'hai già fatto):

    ```bash
    git clone https://github.com/nh-spipitone/CorsoPythonAvanzato.git
    cd CorsoPythonAvanzato
    ```

2. **Crea un ambiente virtuale**:

    ```bash
    python -m venv .venv
    ```

3. **Attiva l'ambiente virtuale**:

    - Windows (PowerShell):
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
    - Linux/macOS:
        ```bash
        source .venv/bin/activate
        ```

4. **Installa le dipendenze** (modalità development):
    ```bash
    pip install -e ".[dev]"
    ```

## 🧪 Test

Per eseguire i test:

```bash
pytest
```

Per eseguire i test con output dettagliato:

```bash
pytest -v
```

## 📁 Struttura del Progetto

```
CorsoPythonAvanzato/
├── Utils/                    # Moduli di utility
│   ├── __init__.py
│   └── sanitization.py      # Funzioni per la normalizzazione del testo
├── esercizi/                # Esercizi pratici
│   └── flask-01/            # Esercizi su Flask
│       └── app.py
├── tests/                   # Test suite
│   └── test_sanitization.py
├── materiale/               # Materiale didattico
├── pyproject.toml           # Configurazione del progetto
├── setup.md                 # Istruzioni di setup
└── README.md                # Questo file
```

## 📚 Moduli

### Utils.sanitization

Il modulo `Utils.sanitization` fornisce funzionalità per la normalizzazione del testo:

#### `normalize_text(s: str, *, tabsize: int = 4, collapse_blank: bool = True) -> str`

Normalizza una stringa applicando le seguenti trasformazioni:

1. Rimuove il BOM (Byte Order Mark)
2. Converte tutti i newline (CRLF, CR) in LF
3. Espande i TAB solo nell'indentazione (non all'interno delle stringhe)
4. Rimuove gli spazi trailing da ogni riga
5. Applica dedent comune preservando la struttura relativa
6. Collassa righe vuote consecutive (se `collapse_blank=True`)
7. Rimuove righe vuote iniziali e finali
8. Garantisce un newline alla fine del file

**Esempio d'uso:**

```python
from Utils.sanitization import normalize_text

raw_text = "\ufeff\tdef foo():\r\n\t\tprint('x')  \r\n\r\n    \treturn 1\r\n"
normalized = normalize_text(raw_text, tabsize=4, collapse_blank=True)
print(normalized)
# Output:
# def foo():
#     print('x')
#
#     return 1
```

## 🛠️ Sviluppo

### Aggiungere Nuovi Test

I test sono organizzati nella cartella `tests/`. Per aggiungere nuovi test:

1. Crea un file `test_*.py` nella cartella `tests/`
2. Importa `pytest` e i moduli da testare
3. Scrivi funzioni di test che iniziano con `test_`
4. Esegui `pytest` per verificare

### Configurazione

Il progetto utilizza `pyproject.toml` per la configurazione:

-   **Build system**: setuptools
-   **Python richiesto**: >= 3.11
-   **Dev dependencies**: pytest >= 8.0

## 📝 Note

-   Il progetto utilizza pytest per il testing con configurazione in `pyproject.toml`
-   L'installazione in modalità editable (`-e`) permette di modificare il codice senza reinstallare
-   I test sono configurati per essere eseguiti dalla cartella `tests/`

## 👥 Autore

Repository gestita da **nh-spipitone**

---

Per domande o problemi, apri un issue nella repository.
