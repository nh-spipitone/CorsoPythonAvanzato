import os
import time
import tkinter as tk
from tkinter import messagebox
import pyotp

# Secret demo: deve combaciare con DEMO_TOTP_SECRET del server
SECRET = os.getenv("TOTP_SECRET", "JBSWY3DPEHPK3PXP")

class Authenticator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Authenticator (TOTP)")
        self.minsize(320, 160)

        self.secret_var = tk.StringVar(value=SECRET)
        self.code_var = tk.StringVar(value="------")
        self.left_var = tk.StringVar(value="30")

        tk.Label(self, text="Secret").pack(anchor="w", padx=12, pady=(12,0))
        tk.Entry(self, textvariable=self.secret_var).pack(fill="x", padx=12)

        box = tk.Frame(self); box.pack(fill="x", padx=12, pady=12)
        tk.Label(box, text="Codice OTP:", font=("Segoe UI", 12, "bold")).pack(side="left")
        tk.Label(box, textvariable=self.code_var, font=("Consolas", 20, "bold")).pack(side="left", padx=8)
        tk.Label(box, textvariable=self.left_var).pack(side="right")

        tk.Button(self, text="Copia", command=self.copy).pack(pady=(0,12))

        self.after(200, self.tick)

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.code_var.get())
        messagebox.showinfo("OK", "Codice copiato negli appunti.")

    def tick(self):
        secret = self.secret_var.get().strip()
        if secret:
            totp = pyotp.TOTP(secret)
            now = time.time()
            # pyotp usa step=30s di default
            remaining = 30 - int(now) % 30
            self.code_var.set(totp.now())
            self.left_var.set(f"{remaining}s")
        self.after(1000, self.tick)

if __name__ == "__main__":
    Authenticator().mainloop()
