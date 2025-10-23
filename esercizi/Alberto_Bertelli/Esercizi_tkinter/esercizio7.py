# Esercizio 7 – Cambia colore di sfondo

# Obiettivo: imparare ad aggiornare dinamicamente la finestra e usare Radiobutton con StringVar.

# Traccia

# Crea tre Radiobutton per scegliere un colore (es. rosso, verde, blu).

# Quando si seleziona un colore, cambia lo sfondo della finestra.

# Mostra in una Label il nome del colore scelto.

import tkinter as tk
from tkinter import ttk,Radiobutton

root = tk.Tk()
root.title('Radiobutton')
root.geometry('500x250')

colore_var =tk.StringVar(value="Nessuno")
# --- Funzione per cambiare colore ---
def cambia_colore():
    colore =colore_var.get()
    if colore== "Rosso":
        root.configure(bg="red")
    elif colore== "Verde":
        root.configure(bg="green")
    elif colore== "Blu":
        root.configure(bg="blue")
    else:
        root.configure(bg="SystemButtonFace")
    label_colore.config(text=f"Hai scelto: {colore}")

# --- Radiobutton ---
ttk.Radiobutton(root, text="Rosso", value="Rosso", variable=colore_var, command=cambia_colore).pack(pady=5)
ttk.Radiobutton(root, text="Verde", value="Verde", variable=colore_var, command=cambia_colore).pack(pady=5)
ttk.Radiobutton(root, text="Blu", value="Blu", variable=colore_var, command=cambia_colore).pack(pady=5)

# --- Etichetta che mostra il colore scelto ---
label_colore = ttk.Label(root, text="Nessun colore selezionato", font=("Arial", 12))
label_colore.pack(pady=20)

# Avvio finestra
root.mainloop()



# import tkinter as tk
# from tkinter import ttk

# def cambia_colore():
# colore = var_colore.get()
# root.configure(bg=colore)
# label_output.config(text=f"Colore scelto: {colore.capitalize()}")

# root = tk.Tk()
# root.title("Cambia colore di sfondo")
# root.geometry("300x200")

# var_colore = tk.StringVar(value="white")

# ttk.Label(root, text="Scegli un colore:").pack(pady=5)

# ttk.Radiobutton(root, text="Rosso", value="red", variable=var_colore, command=cambia_colore).pack()
# ttk.Radiobutton(root, text="Verde", value="green", variable=var_colore, command=cambia_colore).pack()
# ttk.Radiobutton(root, text="Blu", value="blue", variable=var_colore, command=cambia_colore).pack()

# label_output = ttk.Label(root, text="Colore scelto: Nessuno")
# label_output.pack(pady=15)

# root.mainloop()