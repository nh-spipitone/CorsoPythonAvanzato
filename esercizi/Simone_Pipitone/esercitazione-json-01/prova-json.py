import json  # Importa il modulo json per lavorare con dati JSON

# struttura json

esempio = {
    "nome": "Simone",
    "skills": ["python", "django"],
    "active": True,
}  # Crea un dizionario Python con alcuni dati

esempio_json = json.dumps(
    esempio, indent=2
)  # Converte il dizionario in una stringa JSON formattata
print(esempio_json)  # Stampa la stringa JSON

with open(
    "esempio.json", "w", encoding="utf-8"
) as f:  # Apre un file in scrittura con codifica UTF-8
    json.dump(
        esempio, f, indent=2, ensure_ascii=False
    )  # Scrive il dizionario come JSON nel file

with open("esempio.json", "r", encoding="utf-8") as f:  # Apre il file JSON in lettura
    data = json.load(f)  # Carica i dati JSON dal file in una variabile Python
    print(data)  # Stampa il dizionario caricato
    print(type(data))  # Stampa il tipo della variabile (dovrebbe essere dict)
    print(data["nome"])  # Stampa il valore associato alla chiave "nome"
    print(data["skills"][0])  # Stampa il primo elemento della lista "skills"
    print(data["active"])  # Stampa il valore associato alla chiave "active"

data = None  # Inizializza la variabile data a None


with open(
    "esempio.json", "r", encoding="utf-8"
) as f:  # Apre di nuovo il file JSON in lettura
    data = json.loads(
        f.read()
    )  # Legge tutto il contenuto e lo converte da stringa JSON a dizionario Python

if data:  # Se data contiene qualcosa (non è None o vuoto)
    with open(
        "esempio_2.json", "w", encoding="utf-8"
    ) as f:  # Apre un nuovo file in scrittura
        data["skills"].append("flask")  # Aggiunge "flask" alla lista delle skills
        json.dump(
            data, f, indent=2, ensure_ascii=False
        )  # Scrive il nuovo dizionario come JSON nel nuovo file
