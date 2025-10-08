from os import getcwd, makedirs, path, rename, listdir, environ, remove
import json

print(getcwd())

folder_path = "notes"
nota1 = path.join(folder_path, "note1.txt")
nota2 = path.join(folder_path, "note2.txt")
to_rename = path.join(folder_path, "to_rename.txt")
renamed = path.join(folder_path, "renamed.txt")

prima_riga = "Questa è una riga"
seconda_riga = "\nQuesta è la seconda riga"

makedirs(folder_path, exist_ok=True)

with open(to_rename, "w") as f:
    f.write(prima_riga)

# note1
with open(nota1, "w") as f:
    f.write(prima_riga)

# note 2 con seconda riga
with open(nota2, "w") as f:
    f.write(prima_riga)

with open(nota2, "a") as f:
    f.write(seconda_riga)

lista_path = listdir(folder_path)

# mostriamo solo quelli con estensione txt
for name in lista_path:
    if(name.endswith(".txt")):
        print(name)

lista_file_info = []
for file_name in lista_path:
    full_path = path.join(folder_path, file_name)
    size_bytes = path.getsize(full_path)
    lista_file_info.append({
        "name": file_name,
        "size_bytes": size_bytes
    })
    with open(
        "index.json", "w", encoding="utf-8"
    ) as f:
        json.dump(
            lista_file_info, f, ensure_ascii=False
        ) 

with open("index.json", "r", encoding="utf-8") as index_json:
    data1 = json.load(index_json)

with open("index.json", "r", encoding="utf-8") as index_json:
    index_data = index_json.read()

data2 = json.loads(index_data)

print(data1 == data2)

rename(to_rename, renamed)

if environ.get("WS_CLEAN", "1") == "1":
    remove(renamed)
