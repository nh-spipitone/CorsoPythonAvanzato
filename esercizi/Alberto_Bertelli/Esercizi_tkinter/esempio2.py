# import tkinter as tk
# from tkinter import ttk, messagebox

# def calcola(operazione):
# try:
#     a = float(num1.get())
#     b = float(num2.get())
#     if operazione == '+':
#     risultato.set(a + b)
# elif operazione == '-':
#     risultato.set(a - b)
# elif operazione == '*':
# risultato.set(a * b)
# elif operazione == '/':
# risultato.set(a / b)
# except ZeroDivisionError:
# messagebox.showerror("Errore", "Divisione per zero!")
# except ValueError:
# messagebox.showerror("Errore", "Inserisci solo numeri!")

# root = tk.Tk()
# root.title("Calcolatrice Base")

# num1 = tk.StringVar()
# num2 = tk.StringVar()
# risultato = tk.StringVar(value="Risultato qui")
# ttk.Entry(root, textvariable=num1, width=10).grid(row=0, column=0, padx=5)
# ttk.Entry(root, textvariable=num2, width=10).grid(row=0, column=1, padx=5)

# for i, op in enumerate(['+', '-', '*', '/']):
# ttk.Button(root, text=op, command=lambda o=op: calcola(o)).grid(row=1, column=i, padx=5, pady=10)
# tk.Label(root, textvariable=risultato, font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=4, pady=10)

# root.mainloop()