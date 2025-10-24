# Esercizio: Stopwatch (`after`) + Mini‑Paint (Event Binding) — SOLO `.pack`

## Obiettivi

-   Usare `after` / `after_cancel` per un **cronometro** (stopwatch).
-   Allenare i **binding degli eventi** con un mini **paint** su `Canvas`.

Consegna due file: `cronometro.py` e `minipaint.py`.

---

## Parte A — Cronometro con `after` (10–15 min)

**Requisiti**

1. Finestra con titolo `Stopwatch`.
2. Un `Label` grande che mostra il tempo in formato **`MM:SS.D`** (decimi).
3. Quattro pulsanti: **Start**, **Stop**, **Reset**, **Lap** (tutti con `.pack()`).
4. Aggiornamento del display ogni **100 ms** usando `after(100, ...)` **solo quando il cronometro è in esecuzione**.
5. `Lap` aggiunge il tempo corrente in una `Listbox` (numerando i giri).
6. `Reset` ferma tutto e riporta il display a `00:00.0` pulendo anche la `Listbox`.
7. Usa una variabile per conservare l'ID del job `after` così da poterlo annullare con `after_cancel`.

**Suggerimenti rapidi**

-   Conserva uno stato `running` (bool) e un `job` (id dell'`after`).
-   Usa `time.perf_counter()` per misurare il tempo con precisione; memorizza un `start_time` e un `accum` per i secondi accumulati quando metti in pausa.

---

## Parte B — Mini‑Paint (Event Binding) (10–15 min)

**Requisiti**

1. `Canvas` bianco (es. 400×250) e sotto un `Label` di **stato**.
2. Disegna un pallino/cerchio ad ogni **click sinistro** e durante il **trascinamento** (`<Button-1>`, `<B1-Motion>`).
3. Tasti **Freccia SU/GIÙ**: aumentano/diminuiscono la dimensione del pennello (mostra la dimensione nello stato).
4. Tasto **C**: pulisce il canvas.
5. **Doppio click** sul canvas: cambia il colore del pennello (es. nero ↔ blu).
6. Usa solo `.pack()` per il layout.

**Suggerimenti rapidi**

-   Metti il focus sul canvas con `canvas.focus_set()` per ricevere i tasti, oppure usa `bind_all`.
-   Per disegnare un punto: `create_oval(x-r, y-r, x+r, y+r, fill=colore, outline="")`.

---

## Consegna

-   File: `cronometro.py`, `minipaint.py`.
-   SOLO `.pack` per i layout.
-   Commenti essenziali, niente fronzoli.

**Extra (facoltativo)**

-   Aggiungi la scorciatoia **Space** che fa da Start/Stop nel cronometro.
-   Nel mini‑paint, mostra le coordinate correnti nello stato anche su `<Motion>` (senza disegnare).
