import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk


BGPATH=Path(r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\bg.png")
THUMB_SIZE = (120, 120)


class Pokemon:


    def __init__(self,nome,hp,attacco):
        self.nome=nome
        self.hp=hp
        self.attacco=attacco
    
    def stato(self):
        return self.hp >0
    
    def attacca(self):
        pass


class Battaglia_pokemon(tk.Tk):
    

    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
        label_seleziona=tk.Label(self,text="Seleziona il tuo Pokemon",font=('Times 14'))
        label_seleziona.grid(row=0, column=0, pady=(16, 8), sticky="n")
        row=tk.Frame(self,bg="#222")
        row.grid(row=1,column=0,padx=20, pady=12, sticky="nsew")
        row.grid_columnconfigure(0,weight=1)
        row.grid_columnconfigure(4,weight=1)
        for c in (1, 2, 3):
            row.grid_columnconfigure(c, weight=0)
        row.grid_rowconfigure(0,weight=1)
        bg_full = Image.open(BGPATH)
        bg=bg_full.copy().convert("RGBA")

        bg=bg.resize(THUMB_SIZE,Image.LANCZOS)
        for i in range(3):
            btn=tk.Button(row,image=bg,bd=0, highlightthickness=0,cursor="hand2")
            btn.grid(row=0, column=i+1, padx=12, pady=12)

        




app=Battaglia_pokemon()
app.mainloop()