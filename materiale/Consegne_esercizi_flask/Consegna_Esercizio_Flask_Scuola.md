# Esercizio Flask — Registro Scolastico (Voti & Presenze)

## Obiettivo

Realizza una mini web‑app **Flask** che emula un sito scolastico con:

-   elenco studenti,
-   dettaglio studente con **media voti** e **presenze/assenze/ritardi**,
-   moduli per inserire **nuovi voti** e **nuove presenze**,
-   salvataggio su **file JSON** (`db.json`), senza database esterni.

> Usa **solo** Flask + standard library (`json`, `os`, `datetime`).

---

## Requisiti funzionali

1. **Dashboard**
    - `GET /` → mostra conteggio studenti, numero totale voti, presenze registrate nell'intero sistema.
2. **Studenti**
    - `GET /students` → lista studenti (nome, classe) con link al dettaglio.
    - `GET /students/<int:student_id>` → dettaglio con:
        - media voti (2 decimali) e numero di voti,
        - conteggio presenze: presenti / assenti / in ritardo (sommare anche i minuti di ritardo).
3. **Nuovo voto**
    - `GET /students/<id>/grade/new` → form HTML con `materia`, `valore` (0–10, può avere decimali), `data` (YYYY‑MM‑DD).
    - `POST /students/<id>/grade/new` → valida e salva su `db.json`. Redirect al dettaglio.
4. **Nuova presenza**
    - `GET /students/<id>/attendance/new` → form con `data` (YYYY‑MM‑DD), `status` ∈ {`present`, `absent`, `late`}, `minutes_late` (solo se `late`, intero ≥0).
    - `POST /students/<id>/attendance/new` → valida e salva. Redirect al dettaglio.
5. **API JSON**
    - `GET /api/students` → lista studenti (JSON).
    - `GET /api/students/<id>` → dettaglio con voti e presenze.
    - `POST /api/students/<id>/grades` → crea voto (body JSON con `subject`, `value`, `date`). Ritorna `201` con il record.
    - `POST /api/students/<id>/attendance` → crea presenza (body JSON con `date`, `status`, `minutes_late` opzionale). `201` in caso di successo.
6. **Persistenza su file**
    - File: `db.json` nella root del progetto. Se non esiste, crealo con struttura vuota:
        ```json
        { "students": [], "grades": [], "attendance": [] }
        ```
    - Usa `with open(..., "r"/"w", encoding="utf-8")`, `json.load`, `json.dump(indent=2, ensure_ascii=False)`.
7. **Validazione minima**
    - `value` ∈ [0, 10].
    - `date` formato ISO `YYYY-MM-DD`.
    - `status` tra `present`, `absent`, `late`. Se `late`, `minutes_late` richiesto (≥0).
    - Lo `student_id` deve esistere.
8. **UX essenziale**
    - Template `templates/` con:
        - `index.html` (dashboard),
        - `students.html` (lista),
        - `student_detail.html` (dettaglio + link ai form),
        - `form_grade.html`, `form_attendance.html` (form + errori).
    - `static/style.css` minimal per leggibilità.

---

## Vincoli tecnici

-   Usa **solo**: Flask (`render_template`, `request`, `redirect`, `url_for`, `jsonify`), `json`, `os`, `datetime`.
-   Percorsi file con `os.path.join`.
-   Organizza il codice con funzioni helper: `load_db()`, `save_db()`, `next_id(seq)`, `get_student(db, id)`, ecc.

---

## Criteri di valutazione

-   Funzionalità implementate e correttezza delle validazioni.
-   Codice pulito e leggibile (piccole funzioni, niente duplicazione evitabile).
-   Uso corretto di `with open`, `json.load/json.dump` e delle rotte Flask.
-   UX semplice ma chiara (errori visibili, link navigabili).

---

## Bonus (facoltativi)

-   Filtro per classe su `/students?class=3A`.
-   Paginazione voti/presenze sul dettaglio.
-   Esportazione `GET /api/students/<id>/report` con media e breakdown.
-   Tabella media per materia nel dettaglio.

---
