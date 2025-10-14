# Esercitazione 2 Pydantic

Come DB utilizzare una lista o un dizionario locale

## Obiettivo

Costruire una semplice API per la gestione di eventi, con i seguenti campi:

- `title`: testo, minimo 3 caratteri

- `description`: opzionale, max 500 caratteri

- `start`: `datetime`

- `end`: `datetime`, deve essere successiva a start

- `price`: numero ≥ 0

- `participants`: lista di partecipanti, ognuno con:

- - `name`: stringa non vuota

- - `email`: stringa

- - `age`: opzionale, ≥ 0 se presente


# Lista delle Route
- POST	    `/events/`	            ✅ Crea un nuovo evento
- GET	        `/events/{event_id}`	🔍 Recupera i dettagli di un evento specifico tramite il suo UUID
- PATCH	    `/events/{event_id}`	✏️ Aggiorna parzialmente un evento esistente
- DELETE	    `/events/{event_id}`	❌ Elimina un evento
- GET	        `/events/`	            📃 (Opzionale) Restituisce la lista di tutti gli eventi (per test/debug)


#  Dettagli per ciascuna Route
1. POST `/events/`

Input: JSON con i campi dell'evento

Validazioni:

- `title` almeno 3 caratteri

- `price` ≥ 0

- `end` > `start`

- `partecipants`: opzionale, ma se presenti devono avere nome/email validi

Output: evento creato con id generato (UUID)

Status code: 201 Created

2. GET `/events/{event_id}`

Input: `event_id` come UUID

Output: dati dell’evento

Errori: 404 se non trovato

3. PATCH `/events/{event_id}`

Input: solo i campi da aggiornare

Validazioni:

- se start e/o end vengono modificati, assicurarsi che `end` > `start`

Output: evento aggiornato

Errori: 404 se non esiste, 400 se i dati sono invalidi

4. DELETE `/events/{event_id}`

Input: `event_id` come UUID

Output: nessuno (204 No Content)

Errori: 404 se non esiste

5. GET `/events/` (opzionale ma utile)

Output: lista di tutti gli eventi nel "database"