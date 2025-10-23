import tkinter as tk
from tkinter import ttk,messagebox

class minipaint(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini-paint")
        self.geometry("450x300")
        self.canvas=tk.Canvas(self)
        self.canvas.pack()
        self.stateLabel=tk.Label(self)
        self.stateLabel.pack()
    



app=minipaint()
app.mainloop()