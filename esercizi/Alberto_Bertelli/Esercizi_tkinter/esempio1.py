# import tkinter as tk
# from tkinter import ttk, messagebox

# def c_to_f(c):
#     return c * 9/5 + 32

# def converti():
#     try:
#         c = float(var_input.get())
#         f = c_to_f(c)
#     var_output.set(f"{f:.2f} °F")
#     except ValueError:
#     messagebox.showerror("Errore", "Inserisci un numero valido!")

# root = tk.Tk()
# root.title("Convertitore °C → °F")
# root.geometry("300x150")

# var_input = tk.StringVar()
# var_output = tk.StringVar(value="–")

# frame = ttk.Frame(root, padding=16)
# frame.pack()

# ttk.Label(frame, text="°C:").grid(row=0, column=0)
# ttk.Entry(frame, textvariable=var_input).grid(row=0, column=1)
# ttk.Button(frame, text="Converti", command=converti).grid(row=1, column=0, columnspan=2, pady=8)
# ttk.Label(frame, textvariable=var_output, font=("Helvetica", 14, "bold")).grid(row=2, column=0, columnspan=2)

# root.mainloop()