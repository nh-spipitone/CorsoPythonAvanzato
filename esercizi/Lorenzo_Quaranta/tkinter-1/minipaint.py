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
        self.paint_color="black"
    
    def onclick(self):
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.paint_color, outline="")
    
    def change_col(self):
        if self.paint_color=="black":
            self.paint_color="blue" 
        else: self.paint_color="black"


app=minipaint()


app.mainloop()