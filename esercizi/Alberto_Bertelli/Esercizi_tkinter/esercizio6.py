# Esercizio 6 – Seleziona un giorno della settimana

# 🎯 Obiettivo: imparare a usare Combobox (menu a tendina) e mostrare la selezione in tempo reale.

# ✅ Traccia

# Crea una Combobox con i 7 giorni della settimana.

# Quando l’utente seleziona un giorno, mostrane il nome in una Label.


import tkinter as tk
from tkinter import ttk,messagebox

root = tk.Tk()
root.title('Combobox')
root.geometry('500x250')

ttk.Label(root,width=27,text="Esercizio 6",background = 'green', foreground ="white", font = ("Times New Roman", 15)).grid(row = 0, column = 1)

ttk.Label(root, text = "Select the day :",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 5, padx = 10, pady = 25)
n =tk.StringVar()
montchosen= ttk.Combobox(root,width=27,textvariable=n)

montchosen['values']=('lunedì',
                      'martedì',
                      'mercoledì',
                      'giovedì',
                      'venerdì',
                      'sabato',
                      'domenica')
montchosen.grid(column=1,row=5)
montchosen.current()
root.mainloop()





# import tkinter as tk
# from tkinter import ttk

# def mostra_giorno(event):
# giorno = var_giorno.get()
# label_output.config(text=f"Hai scelto: {giorno}")

# root = tk.Tk()
# root.title("Giorno della settimana")
# root.geometry("300x200")

# var_giorno = tk.StringVar()

# ttk.Label(root, text="Scegli un giorno:").pack(pady=5)
# combo = ttk.Combobox(root, textvariable=var_giorno, state="readonly")
# combo["values"] = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
# combo.pack(pady=5)

# label_output = ttk.Label(root, text="Nessun giorno selezionato")
# label_output.pack(pady=10)

# combo.bind("<<ComboboxSelected>>", mostra_giorno)

# root.mainloop()