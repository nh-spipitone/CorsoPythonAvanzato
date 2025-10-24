import tkinter as tk
from tkinter import ttk,messagebox
import time

import pyotp

SECRET_KEY="cambiami"

class Authenticator(tk.Tk):
    #funzioni helper
    def generate_otp(self):
        secret_txt=self.secret.get()
        if secret_txt:
            totp=pyotp.TOTP(secret_txt)
            now=time.time()
            remaining=self.time.get()-int(now)%30
            self.code.set(totp.now())
            self.remaining.set(remaining)
        self.after(1000,self.generate_otp)


    def copy_otp(self):
        self.clipboard_clear()
        self.clipboard_append(self.code.get())
        messagebox.showinfo("informazione","codice copiato negli appunti")

    def __init__(self):
        super().__init__()
        self.title("OTP Authenticator")
        self.minsize(320,160)
        self.geometry("480x300")
        #variabili di stato
        self.secret=tk.StringVar(value= SECRET_KEY)
        self.code=tk.StringVar(value="------")
        self.time=tk.IntVar(value= 30)
        self.remaining=tk.IntVar(value= 30)

        #Interfaccia grafica
        self.header=tk.Label(self,text="Codice OTP:",font=("Segoe UI", 20, "bold"))
        self.header.pack()
        self.otp_text=tk.Label(self,textvariable=self.code, font=("Consolas", 25, "bold"))
        self.otp_text.pack()
        self.timer=ttk.Progressbar(self,orient="horizontal",mode="determinate",length=300,maximum=30,variable=self.remaining)
        self.timer.pack()
        self.copy=tk.Button(self,text="copia",command=self.copy_otp)
        self.copy.pack()
        self.after(200, self.generate_otp())

app=Authenticator()
app.mainloop()    
        
