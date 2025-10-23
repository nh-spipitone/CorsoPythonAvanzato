# Esercizio 5 – Contatore di click

# Obiettivo: far capire come aggiornare dinamicamente un’etichetta (Label) ogni volta che l’utente preme un pulsante.

# ✅ Specifiche

# Crea una finestra Tkinter con un’etichetta che mostri il numero di click.

# Crea un pulsante “Aumenta” che incrementa il contatore.

# Crea un pulsante “Azzera” che riporta il contatore a 0.



import tkinter as tk
from tkinter import ttk,messagebox

root =tk.Tk()
root.title("Contatore di click")
var_output =tk.StringVar(value="Contatore:0")
cont =0



def incrementa():
    global cont
    cont +=1
    var_output.set(f"Contatore: {cont}")

def azzera():
    global cont
    cont = 0
    var_output.set(f"Contatore: {cont}")




ttk.Label(root, textvariable=var_output, font=("Arial", 16)).pack(pady=20)
ttk.Button(root, text="Incrementa", command=incrementa).pack(pady=10)
ttk.Button(root, text="Azzera", command=azzera).pack(pady=10)
root.mainloop()



# import tkinter as tk
# from tkinter import ttk

# def incrementa():
# contatore.set(contatore.get() + 1)

# def azzera():
# contatore.set(0)

# root = tk.Tk()
# root.title("Contatore di click")
# root.geometry("250x200")

# contatore = tk.IntVar(value=0)

# ttk.Label(root, text="Numero di click:").pack(pady=10)
# ttk.Label(root, textvariable=contatore, font=("Helvetica", 16, "bold")).pack(pady=10)

# ttk.Button(root, text="Aumenta", command=incrementa).pack(pady=5)
# ttk.Button(root, text="Azzera", command=azzera).pack(pady=5)

# root.mainloop()
