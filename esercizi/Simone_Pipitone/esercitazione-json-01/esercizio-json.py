# file: mini_workspace.py
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Carica le variabili d'ambiente dal file .env


def main():
    # 1) CWD
    cwd = os.getcwd()
    print("CWD:", cwd)

    # 2) Root da env o CWD
    root = os.environ.get("WS_ROOT", "notes") or cwd
    print("Root:", root)

    # 3) notes/
    notes_dir = os.path.join(root, "notes")
    os.makedirs(notes_dir, exist_ok=True)

    # 4) Crea file .txt
    nota1 = os.path.join(notes_dir, "nota1.txt")
    nota2 = os.path.join(notes_dir, "nota2.txt")
    to_rename = os.path.join(notes_dir, "to_rename.txt")

    with open(nota1, "w", encoding="utf-8") as f:
        f.write("Prima riga di nota1\n")

    with open(nota2, "w", encoding="utf-8") as f:
        f.write("Prima riga di nota2\n")
    # append su nota2
    with open(nota2, "a", encoding="utf-8") as f:
        f.write("Seconda riga (append) di nota2\n")

    with open(to_rename, "w", encoding="utf-8") as f:
        f.write("File che verrà rinominato\n")

    # 5) Elenco .txt
    print("\nFile in notes/:")
    for name in os.listdir(notes_dir):
        if name.lower().endswith(".txt"):
            print(" -", name)

    # 6) Indice (name, size_bytes)
    index = []
    for name in os.listdir(notes_dir):
        if name.lower().endswith(".txt"):
            fp = os.path.join(notes_dir, name)
            size = os.path.getsize(fp)
            index.append({"name": name, "size_bytes": size})

    # 7) Salva index.json nella root
    index_path = os.path.join(root, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print("\nScritto:", index_path)

    # 8) Letture JSON: load vs loads
    with open(index_path, "r", encoding="utf-8") as f:
        data_a = json.load(f)  # file -> Python

    with open(index_path, "r", encoding="utf-8") as f:
        s = f.read()
    data_b = json.loads(s)  # stringa -> Python

    print("Elementi (load):", len(data_a))
    print("Elementi (loads):", len(data_b))
    print("Coincidono:", data_a == data_b)

    # 9) Rinomina
    renamed = os.path.join(notes_dir, "renamed.txt")
    os.rename(to_rename, renamed)
    print("Rinominato to_rename.txt -> renamed.txt")
    print("Torename", to_rename)
    print("Renamed", renamed)
    # 10) Cleanup opzionale
    print(os.environ.get("WS_CLEAN") == "3")
    if os.environ.get("WS_CLEAN") == "3":
        if os.path.exists(renamed):
            os.remove(renamed)
            print("Cleanup: removed renamed.txt")


if __name__ == "__main__":
    main()
