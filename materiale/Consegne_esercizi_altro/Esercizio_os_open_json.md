# Esercizio – Mini workspace, file `.txt` e indice JSON (solo `os`, `open`, `json`)

## Obiettivo
Creare una piccola struttura di file, manipolarla con la libreria **os**, leggere/scrivere file con **open**, e produrre/leggere un indice in **JSON**. Niente `pathlib`: usa **os**, **os.path**, **open**, **json**.

---

## Requisiti funzionali
1. **Stampa CWD** – Mostra a schermo la cartella corrente con `os.getcwd()`.
2. **Root di lavoro** – Se esiste la variabile d'ambiente `WS_ROOT`, usala come root; altrimenti usa la CWD.
3. **Creazione cartella** – Crea `notes/` dentro la root (`os.makedirs(..., exist_ok=True)`).
4. **File di testo** – Crea in `notes/` i seguenti file con `open(..., "w")`:
   - `nota1.txt` con almeno una riga.
   - `nota2.txt` con almeno una riga, poi aprilo in **append** (`"a"`) e aggiungi una seconda riga.
   - `to_rename.txt` con almeno una riga.
5. **Lista contenuti** – Elenca i file presenti in `notes/` con `os.listdir(...)` e stampa **solo** quelli che terminano con `.txt`.
6. **Indice JSON** – Costruisci una lista di dizionari con chiavi:
   - `name`: il nome del file (stringa).
   - `size_bytes`: la dimensione del file in byte (usa `os.path.getsize`).
   Salva l'indice in `index.json` nella **root** usando `with open(..., "w", encoding="utf-8")` + `json.dump(..., indent=2, ensure_ascii=False)`.
7. **Lettura JSON (A & B)** – Riapri `index.json` e leggi i dati:
   - (A) con `json.load(f)`
   - (B) con `json.loads(f.read())`
   Stampa il numero di elementi per entrambe le letture e verifica che `data_a == data_b`.
8. **Rinomina** – Rinomina `to_rename.txt` in `renamed.txt` usando `os.rename(src, dst)`.
9. **Cleanup opzionale** – Se la variabile d'ambiente `WS_CLEAN` vale `"1"`, elimina `renamed.txt` con `os.remove(...)` (se esiste).

---

## Vincoli tecnici (match al ripasso)
- Usa **solo**: `os`, `os.path`, `open`, `json`.
- Funzioni attese: `os.getcwd`, `os.listdir`, `os.makedirs(..., exist_ok=True)`, `os.remove`, `os.rename`, `os.environ.get`, `os.path.join`, `os.path.getsize`.
- File I/O con `with open(..., encoding="utf-8")`: modalità `"w"`, `"a"`, `"r"`.
- JSON: `json.dump`, `json.load`, `json.dumps`, `json.loads` (quest’ultimo **solo** per il punto 7B).

---

## Output atteso a schermo (esempio indicativo)
```
CWD: /percorso/assoluto
Root: /percorso/assoluto
File in notes/:
 - nota1.txt
 - nota2.txt
 - to_rename.txt
Scritto: /percorso/assoluto/index.json
Elementi (load): 3
Elementi (loads): 3
Coincidono: True
Rinominato to_rename.txt -> renamed.txt
(Se WS_CLEAN=1) Cleanup: removed renamed.txt
```

---

## Suggerimenti
- Per comporre percorsi usa **solo** `os.path.join(root, "notes")`, ecc.
- Ricordati `encoding="utf-8"` in tutte le aperture file.
- `ensure_ascii=False` evita gli escape `\uXXXX` per accenti/emoji.
- Controlla l’estensione con `name.lower().endswith(".txt")`.

---

## Bonus (facoltativi)
- Aggiungi variabile d’ambiente `MAX_FILES`: se presente, limita l’indice ai primi *N* file `.txt` trovati.
- Crea un file `run.log` nella root e in **append** (`"a"`) scrivi una riga del tipo: `Scansione su <root> - <N> file - OK`.

---

## Consegna
- File Python: `mini_workspace.py` (nessuna libreria esterna).
- Niente soluzioni nel file di consegna; commenti brevi ammessi.
- Verifica che lo script crei/modifichi i file richiesti e stampi l’output atteso.

---

## Come eseguire
```bash
# Esecuzione base (root = CWD)
python mini_workspace.py

# Con root personalizzata (Linux/macOS)
WS_ROOT="/percorso/progetto" python mini_workspace.py

# Con root personalizzata (Windows CMD)
set WS_ROOT=C:\percorso\progetto && python mini_workspace.py

# Cleanup opzionale
WS_CLEAN=1 python mini_workspace.py
```
