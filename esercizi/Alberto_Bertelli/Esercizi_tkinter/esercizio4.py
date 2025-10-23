# Esercizio 4 – Calcolo del quadrato di un numero


# ✅ Specifiche

# Crea un campo di input (Entry) dove l’utente inserisce un numero.

# Aggiungi un pulsante “Calcola quadrato”.

# Mostra il risultato in una Label.

# Se l’utente inserisce testo non numerico, mostra un messagebox di errore.

import tkinter as tk
from tkinter import ttk,messagebox

root =tk.Tk()
root.title("Calcolo del quadrato di un numero")


def calcola(operazione):
    try:
        a = int(num.get())
        risultato.set(a*a)
    except ValueError:
        messagebox.showerror("Error","Inserisci solo i numeri")


num=tk.StringVar()
risultato =tk.StringVar(value="Risultato qui")
ttk.Entry(root,textvariable=num,width=10).grid(row=0,column=8,padx=5)
ttk.Button(root, text="premi", command=lambda o=0: calcola(o)).grid(row=1, column=1, padx=5, pady=10)   
tk.Label(root, textvariable=risultato, font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=4, pady=10)

root.mainloop()



# import tkinter as tk
# from tkinter import ttk, messagebox

# def calcola_quadrato():
# try:
# n = float(var_input.get())
# quadrato = n ** 2
# var_output.set(f"Risultato: {quadrato:.2f}")
# except ValueError:
# messagebox.showerror("Errore", "Inserisci un numero valido!")

# root = tk.Tk()
# root.title("Calcola il quadrato")                                                            SOLUZIONE
# root.geometry("300x200")

# var_input = tk.StringVar()
# var_output = tk.StringVar(value="Risultato: —")

# ttk.Label(root, text="Inserisci un numero:").pack(pady=5)
# ttk.Entry(root, textvariable=var_input).pack(pady=5)
# ttk.Button(root, text="Calcola quadrato", command=calcola_quadrato).pack(pady=10)
# ttk.Label(root, textvariable=var_output, font=("Helvetica", 12, "bold")).pack(pady=10)

# root.mainloop()