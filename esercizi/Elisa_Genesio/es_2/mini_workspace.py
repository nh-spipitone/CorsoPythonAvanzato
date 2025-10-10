import os
import json

# 1 CWD
cwd = os.getcwd()
print(f"CWD: {cwd}")

# 2 Root di lavoro
root = os.environ.get("WS_ROOT", cwd)
print(f"Root: {root}")

# 3 Crea cartella notes/
notes_dir = os.path.join(root, "notes")
os.makedirs(notes_dir, exist_ok=True)

# 4 Crea file di testo
nota1 = os.path.join(notes_dir, "nota1.txt")
nota2 = os.path.join(notes_dir, "nota2.txt")
to_rename = os.path.join(notes_dir, "to_rename.txt")

with open(nota1, "w", encoding="utf-8") as f:
    f.write("Questa è la prima nota.\n")

with open(nota2, "w", encoding="utf-8") as f:
    f.write("Prima riga di nota2.\n")

# Append seconda riga
with open(nota2, "a", encoding="utf-8") as f:
    f.write("Seconda riga aggiunta.\n")

with open(to_rename, "w", encoding="utf-8") as f:
    f.write("File che sarà rinominato.\n")

# 5 Lista contenuti
files = [f for f in os.listdir(notes_dir) if f.lower().endswith(".txt")]
print("File in notes/:")
for f in files:
    print(f" - {f}")

# 6 Indice JSON
index = []
for name in files:
    path = os.path.join(notes_dir, name)
    size = os.path.getsize(path)
    index.append({"name": name, "size_bytes": size})

index_path = os.path.join(root, "index.json")
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)
print(f"Scritto: {index_path}")

# 7 Lettura JSON
# (A)
with open(index_path, "r", encoding="utf-8") as f:
    data_a = json.load(f)

# (B)
with open(index_path, "r", encoding="utf-8") as f:
    data_b = json.loads(f.read())

print(f"Elementi (load): {len(data_a)}")
print(f"Elementi (loads): {len(data_b)}")
print(f"Coincidono: {data_a == data_b}")

# 8 Rinomina
src = to_rename
dst = os.path.join(notes_dir, "renamed.txt")
os.rename(src, dst)
print("Rinominato to_rename.txt -> renamed.txt")

# 9 Cleanup
if os.environ.get("WS_CLEAN") == "1":
    if os.path.exists(dst):
        os.remove(dst)
        print("Cleanup: removed renamed.txt")

# BONUS: run.log
log_path = os.path.join(root, "run.log")
with open(log_path, "a", encoding="utf-8") as log:
    log.write(f"Scansione su {root} - {len(files)} file - OK\n")
