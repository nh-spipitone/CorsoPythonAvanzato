# Mini‑Esercizio Flask (livello ++): Guestbook con template, validazione e salvataggio su file

## Obiettivo

Realizza una piccola web‑app con Flask che permetta di inserire e visualizzare messaggi (guestbook). Userai **template Jinja** con `render_template`, **flash messages**, **redirect dopo POST**, e **persistenza su file JSON**.

---

## Requisiti funzionali (obbligatori)

1. **Home** `GET /`

    - Mostra gli ultimi 20 messaggi (ordinati dal più recente).
    - Link “Scrivi un messaggio”.
    - Se ci sono più di 20 messaggi, mostra paginazione semplice: `?page=1,2,...` (10 per pagina è ok).

2. **Nuovo messaggio** `GET /new`

    - Form con campi: `author` (max 30), `text` (max 200).
    - Protezione base contro XSS: **non** usare `|safe` nelle variabili; l’escape automatico di Jinja basta.

3. **Invio** `POST /new`

    - Validazioni: campi non vuoti, lunghezze rispettate.
    - Se ok: salva il messaggio su file `data/messages.json` (crea la cartella se non esiste), assegna `id` incrementale e **redirect** a `/`.
    - Se errori: **flash** con messaggio e ritorno al form (status 400).

4. **Dettaglio** `GET /msg/<int:msg_id>`

    - Mostra un singolo messaggio. Se non esiste: **404** personalizzata.

5. **Struttura con template** (`render_template`)

    - `base.html` con blocchi, `home.html`, `new.html`, `show.html`, `404.html`.
    - Integra il sistema `flash` per gli errori.

6. **Pulizia & UX**
    - Nessun crash su input non valido.
    - Messaggi d’errore chiari.
    - Link di navigazione di base (Home, Nuovo).

---

## Extra (scegline almeno 2)

-   **Counter visite** in sessione: mostra “Hai visitato N volte”.
-   **Filtro Jinja custom**: es. `truncate_italian(text, n)` per troncare con ellissi.
-   **Ricerca**: su `GET /?q=...` filtra per `author` o testo.
-   **Dark mode** very‑basic (classe CSS toggle via `?theme=dark`).
-   **Export JSON**: rotta `GET /export.json` che restituisce i messaggi.

> Nota: non serve autenticazione. Mantieni il codice leggibile e commentato.

---
