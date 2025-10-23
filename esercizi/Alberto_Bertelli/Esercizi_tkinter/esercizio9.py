# Esercizio – Seleziona gli ingredienti della pizza

# Obiettivo: imparare a usare Checkbutton, variabili Tk (BooleanVar()) e aggiornare dinamicamente la UI in base alle selezioni.

# Traccia

# Crea una finestra con diversi Checkbutton per scegliere gli ingredienti della pizza.

# Ogni Checkbutton rappresenta un ingrediente (es. Mozzarella, Pomodoro, Funghi, ecc.).

# Mostra il totale degli ingredienti selezionati in una Label.

# Aggiungi un pulsante "Mostra scelta" che mostri un messaggio con gli ingredienti selezionati.

import tkinter as tk
from tkinter import ttk, messagebox

# Finestra principale
root = tk.Tk()
root.title("Pizza Ingredients")
root.geometry("400x300")

# Titolo
ttk.Label(
    root,
    width=30,
    text="Esercizio 6 – Seleziona gli ingredienti",
    background='green',
    foreground='white',
    font=("Times New Roman", 14)
).pack(pady=10)

# --- Variabili BooleanVar() per ogni ingrediente ---
mozzarella = tk.BooleanVar()
pomodoro = tk.BooleanVar()
funghi = tk.BooleanVar()
salame = tk.BooleanVar()
cipolla = tk.BooleanVar()

# --- Funzione per aggiornare il totale ---
def aggiorna_totale():
    count = sum([
        mozzarella.get(),
        pomodoro.get(),
        funghi.get(),
        salame.get(),
        cipolla.get()
    ])
    var_totale.set(f"Ingredienti selezionati: {count}")

# --- Funzione per mostrare la scelta ---
def mostra_scelta():
    selezionati = []
    if mozzarella.get(): selezionati.append("Mozzarella")
    if pomodoro.get(): selezionati.append("Pomodoro")
    if funghi.get(): selezionati.append("Funghi")
    if salame.get(): selezionati.append("Salame")
    if cipolla.get(): selezionati.append("Cipolla")

    if selezionati:
        messagebox.showinfo("La tua pizza", f"Hai scelto: {', '.join(selezionati)}")
    else:
        messagebox.showwarning("Nessuna scelta", "Non hai selezionato nessun ingrediente.")

# --- Checkbutton per ogni ingrediente ---
ttk.Checkbutton(root, text="Mozzarella", variable=mozzarella, command=aggiorna_totale).pack(anchor='w', padx=40)
ttk.Checkbutton(root, text="Pomodoro", variable=pomodoro, command=aggiorna_totale).pack(anchor='w', padx=40)
ttk.Checkbutton(root, text="Funghi", variable=funghi, command=aggiorna_totale).pack(anchor='w', padx=40)
ttk.Checkbutton(root, text="Salame", variable=salame, command=aggiorna_totale).pack(anchor='w', padx=40)
ttk.Checkbutton(root, text="Cipolla", variable=cipolla, command=aggiorna_totale).pack(anchor='w', padx=40)

# --- Label per mostrare il totale ---
var_totale = tk.StringVar(value="Ingredienti selezionati: 0")
ttk.Label(root, textvariable=var_totale, font=("Arial", 11)).pack(pady=10)

# --- Pulsante per mostrare riepilogo ---
ttk.Button(root, text="Mostra scelta", command=mostra_scelta).pack(pady=10)

# Avvio
root.mainloop()
