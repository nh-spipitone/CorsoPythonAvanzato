# Esercizio 2 – Agenda Giornaliera

# Obiettivo: esercitarsi con Listbox, Entry, Button e la gestione dinamica dei widget.

# ✳️ Consegnare:

# Crea una piccola app “Agenda Giornaliera” che permetta di aggiungere attività a una lista e rimuoverle.

# 🔧 Requisiti:

# Campo Entry per scrivere un’attività.

# Pulsante “Aggiungi” → inserisce l’attività nella Listbox.

# Pulsante “Elimina” → rimuove l’attività selezionata.

# Messaggio di errore se si tenta di aggiungere una stringa vuota o eliminare senza selezionare nulla.
import tkinter as tk
from tkinter import messagebox

# Creazione finestra principale
root = tk.Tk()
root.title("Agenda Giornaliera")
root.geometry("350x350")
root.resizable(False, False)

# --- Funzioni ---
def aggiungi_attivita():
    attivita = entry_attivita.get().strip()
    if not attivita:
        messagebox.showwarning("Errore", "Inserisci un'attività prima di aggiungere.")
        return
    listbox.insert(tk.END, attivita)
    entry_attivita.delete(0, tk.END)

def elimina_attivita():
    try:
        indice = listbox.curselection()[0]
        listbox.delete(indice)
    except IndexError:
        messagebox.showwarning("Errore", "Seleziona un'attività da eliminare.")

# --- Interfaccia ---
frame = tk.Frame(root)
frame.pack(pady=20)

# Entry per l'attività
entry_attivita = tk.Entry(frame, width=30, font=("Arial", 12))
entry_attivita.grid(row=0, column=0, padx=5)

# Pulsante "Aggiungi"
btn_aggiungi = tk.Button(frame, text="Aggiungi", width=10, command=aggiungi_attivita)
btn_aggiungi.grid(row=0, column=1, padx=5)

# Listbox per le attività
listbox = tk.Listbox(root, width=45, height=10, font=("Arial", 11))
listbox.pack(pady=10)

# Pulsante "Elimina"
btn_elimina = tk.Button(root, text="Elimina", width=10, command=elimina_attivita)
btn_elimina.pack(pady=5)

# Avvio del loop principale
root.mainloop()


