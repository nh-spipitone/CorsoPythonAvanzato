# Esercizio 11 – Carrello della spesa con calcolo totale
# Obiettivo: Creare una lista interattiva di acquisti con prezzi e calcolare il totale in tempo reale.
# Traccia:Crea una finestra con una lista di prodotti e i loro prezzi.

# Aggiungi Checkbutton accanto a ciascun prodotto, in modo che l'utente possa selezionare gli articoli da aggiungere al carrello.

# Mostra il totale (somma dei prezzi degli articoli selezionati) in una Label.

# Aggiungi un pulsante "Aggiungi al carrello" che aggiorna il totale.


import tkinter as tk
from tkinter import ttk, messagebox

# Finestra principale
root = tk.Tk()
root.title("Carrello della spesa con calcolo totale")
root.geometry("400x350")

# Titolo
ttk.Label(
    root,
    width=40,
    text="Esercizio 11 – Seleziona gli articoli",
    background='green',
    foreground='white',
    font=("Times New Roman", 14)
).pack(pady=10)

# Dizionario prodotti con prezzi (€)
prodotti = {
    "Banane": 1.50,
    "Mele": 1.20,
    "Zucchero": 2.00,
    "Acqua": 0.80,
    "Prosciutto": 3.50
}

# Variabili BooleanVar per i Checkbutton
variabili = {nome: tk.BooleanVar() for nome in prodotti}

# Funzione per aggiornare il totale in tempo reale
def aggiorna_totale():
    totale = 0
    for nome, var in variabili.items():
        if var.get():
            totale += prodotti[nome]
    var_totale.set(f"Totale carrello: € {totale:.2f}")

# Funzione per mostrare il riepilogo del carrello
def mostra_carrello():
    selezionati = [nome for nome, var in variabili.items() if var.get()]
    if selezionati:
        totale = sum(prodotti[nome] for nome in selezionati)
        elenco = "\n".join([f"{nome} - € {prodotti[nome]:.2f}" for nome in selezionati])
        messagebox.showinfo("Il tuo carrello", f"Hai selezionato:\n{elenco}\n\nTotale: € {totale:.2f}")
    else:
        messagebox.showwarning("Carrello vuoto", "Non hai selezionato nessun articolo!")

# Creazione dei Checkbutton con prezzi
for nome, prezzo in prodotti.items():
    ttk.Checkbutton(
        root,
        text=f"{nome} - € {prezzo:.2f}",
        variable=variabili[nome],
        command=aggiorna_totale
    ).pack(anchor='w', padx=40)

# Label per mostrare il totale
var_totale = tk.StringVar(value="Totale carrello: € 0.00")
ttk.Label(root, textvariable=var_totale, font=("Arial", 12)).pack(pady=10)

# Pulsante per mostrare il riepilogo
ttk.Button(root, text="Aggiungi al carrello", command=mostra_carrello).pack(pady=10)

# Avvio finestra
root.mainloop()


    