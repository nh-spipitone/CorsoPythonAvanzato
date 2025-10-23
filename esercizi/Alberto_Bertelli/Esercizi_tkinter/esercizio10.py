# Esercizio 10 – Finestra di login
# Obiettivo: Creare una semplice finestra di login dove l'utente può inserire nome utente e password.
# Traccia:
# Crea una finestra con due campi di input: uno per il nome utente e uno per la password.

# Aggiungi un pulsante "Login".

# Quando l'utente clicca su "Login", verifica se il nome utente e la password sono corretti.

# Mostra un messaggio di benvenuto o un messaggio di errore a seconda che i dati inseriti siano corretti o meno.


import tkinter as tk
from tkinter import ttk, messagebox

# Finestra principale
root = tk.Tk()
root.title("Finestra di login")
root.geometry("400x300")

# Quando viene premuto il pulsante “Login”, questa funzione:

# Legge il testo inserito nei campi di input (.get()).

# Confronta i valori con le credenziali fisse (admin / password).

# Se coincidono → mostra un messaggio di successo.

# Altrimenti → mostra un messaggio di errore.
def validate_login():
    userid=username_entry.get()
    password=password_entry.get()
    if userid =="admin" and password== "password":
        messagebox.showinfo("Login effettuato","Benvenuto admin")
    else:
        messagebox.showerror("Login fallito","Invalid username o password")


# Crea un’etichetta “Userid” e un campo di testo per inserire il nome utente.

# .pack() posiziona i widget verticalmente (uno sotto l’altro).

# Stessa cosa per la password, ma con show="*" che nasconde i caratteri digitati (effetto password).

username_label=tk.Label(root, text="Userid")
username_label.pack()
username_entry=tk.Entry(root)
username_entry.pack()
password_label=tk.Label(root,text="Password")
password_label.pack()
password_entry=tk.Entry(root,show="*")
password_entry.pack()
login_button=tk.Button(root,text="Login",command=validate_login)
login_button.pack()
root.mainloop()
