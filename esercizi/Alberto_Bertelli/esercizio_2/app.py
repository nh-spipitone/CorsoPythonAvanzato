import os
import json


#1. **Stampa CWD** – Mostra a schermo la cartella corrente con `os.getcwd()`.
cwd=os.getcwd()
print(cwd)

#2. **Root di lavoro** – Se esiste la variabile d'ambiente `WS_ROOT`, usala come root; altrimenti usa la CWD.
print(os.environ.get("WS_ROOT"))


#3. **Creazione cartella** – Crea `notes/` dentro la root (`os.makedirs(..., exist_ok=True)`)
os.makedirs("notes",exist_ok=True)
notes_dir=os.environ.get("WS_ROOT","notes")


# #4. **File di testo** – Crea in `notes/` i seguenti file con `open(..., "w")`:
#    - `nota1.txt` con almeno una riga.
#    - `nota2.txt` con almeno una riga, poi aprilo in **append** (`"a"`) e aggiungi una seconda riga.
#    - `to_rename.txt` con almeno una riga.

nota1 = os.path.join(notes_dir,"nota1.txt")
nota2 = os.path.join(notes_dir,"nota2.txt")
to_rename = os.path.join(notes_dir,"to_rename.txt")

with open(nota1,"w",encoding="utf=8") as f1:
    f1.write("Questa è una riga")

with open(nota2,"w",encoding="utf=8") as f2:
    f2.write("Questa è un'altra riga") 

with open(to_rename,"w",encoding="utf=8") as f3:
    f3.write("Questa è l'ennesima riga") 


# 5. **Lista contenuti** – Elenca i file presenti in `notes/` con `os.listdir(...)` e stampa **solo** quelli che terminano con `.txt`.

files=os.listdir(notes_dir)
print(os.listdir(notes_dir))

for file in files:
    if(file.lower().endswith(".txt")):
        print(file) 

# 6. **Indice JSON** – Costruisci una lista di dizionari con chiavi:
#    - `name`: il nome del file (stringa).
#    - `size_bytes`: la dimensione del file in byte (usa `os.path.getsize`).
#    Salva l'indice in `index.json` nella **root** usando `with open(..., "w", encoding="utf-8")` + `json.dump(..., indent=2, ensure_ascii=False)`.
lista_diz=[]

for file in files:
    file_path=os.path.join(notes_dir,file)
    dim= os.path.getsize()
    lista_diz.append({"nome":file,"size_bytes":dim})

index_path=os.path.join(notes_dir,"index.json")
with open(index_path,"w",encoding="utf=8") as index_json:
    json.dump(lista_diz,index_json,indent=2,ensure_ascii=False)

# 7. **Lettura JSON (A & B)** – Riapri `index.json` e leggi i dati:
#    - (A) con `json.load(f)`
#    - (B) con `json.loads(f.read())`
#    Stampa il numero di elementi per entrambe le letture e verifica che `data_a == data_b`.

with open(index_path,"w",encoding="utf=8") as index_json:
       data_1=json.load(index_json)
       

with open(index_path,"w",encoding="utf=8") as index_json:
    index_data=index_json.read()
      
data_2=json.loads(index_data)
print(len(data_1))
print(len(data_2))   
print("Coincidono:", data_1 == data_2)  


# 8. **Rinomina** – Rinomina `to_rename.txt` in `renamed.txt` usando `os.rename(src, dst)`.

os.rename(to_rename,"renamed.txt")


# 9. **Cleanup opzionale** – Se la variabile d'ambiente `WS_CLEAN` vale `"1"`, elimina `renamed.txt` con `os.remove(...)` (se esiste).

if(os.environ.get("WS_CLEAN")=="1"):
    os.remove(to_rename)