# Esercizio 2 – Timer con conto alla rovescia

# Obiettivo: creare un'app che mostri un timer con un conto alla rovescia, in modo che l'utente possa avviare e fermare il timer.

# Traccia

# Crea una finestra con un campo di input (per impostare il tempo in secondi).

# Aggiungi un pulsante "Avvia" che avvia il timer (conto alla rovescia).

# Mostra il tempo rimanente in una Label.

# Aggiungi un pulsante "Ferma" per fermare il timer in qualsiasi momento.

# Se il timer arriva a 0, mostra un messaggio di avviso usando messagebox


import tkinter as tk
from tkinter import ttk,messagebox

root =tk.Tk()
root.title("Timer con conto alla rovescia")

# --- Variabili ---
tempo_rimanente = 0
timer_attivo = False
var_output =tk.StringVar(value="Timer:0")


def start():
    """Avvia il conto alla rovescia"""
    global timer_attivo,tempo_rimanente
    if timer_attivo:
        return
    try:
        tempo_rimanente =int(entry_tempo.get())
    except:
        messagebox.showwarning("Errore", "Inserisci un numero valido di secondi.")
        return
    if tempo_rimanente <= 0:
        messagebox.showwarning("Errore", "Inserisci un numero maggiore di 0.")
        return

    timer_attivo = True
    countdown()

def countdown():
    """Aggiorna il timer ogni secondo"""
    global tempo_rimanente, timer_attivo
    if not timer_attivo:
        return
    var_output.set(f"Timer: {tempo_rimanente}")
    if tempo_rimanente > 0:
        tempo_rimanente -= 1
        root.after(1000, countdown)  # richiama countdown ogni 1 secondo
    else:
        timer_attivo = False
        messagebox.showinfo("Tempo scaduto", "Il timer è terminato!")

def stop():
    """Ferma il timer"""
    global timer_attivo
    timer_attivo=False
    var_output.set(f"Timer fermato a: {tempo_rimanente}")


# --- Interfaccia grafica ---
ttk.Label(root, text="Inserisci tempo (sec):").pack(pady=10)
entry_tempo = ttk.Entry(root, width=10)
entry_tempo.pack()
ttk.Label(root, textvariable=var_output, font=("Arial", 16)).pack(pady=20)
ttk.Button(root, text="Start", command=start).pack(pady=10)
ttk.Button(root, text="stop", command=stop).pack(pady=10)

root.mainloop()