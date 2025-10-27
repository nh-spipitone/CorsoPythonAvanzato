import tkinter as tk
from tkinter import ttk,messagebox

class minipaint(tk.Tk):
    
    def onclick_paint (self,event):
            r=self.brush_radius
            self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill=self.paint_color, outline="")
    
    def change_col(self,event):
        if self.paint_color=="black":
            self.paint_color="blue" 
        else: self.paint_color="black"

    def clear_canvas(self,event):
         print("arriva?")
         self.canvas.delete("all")
         
    def change_brush_size(self,event):
        print("arriva?")
        key=event.keysym
        
        if key=="Up":
             self.brush_radius+=1
        elif key=="Down":
            if self.brush_radius>1:
                self.brush_radius-=1
        self.stateString.set("Dimensione pennello:" +str(self.brush_radius))   
    
    def __init__(self):
        super().__init__()
        self.title("Mini-paint")
        self.geometry("450x350")
        self.canvas=tk.Canvas(self,width=450,height=300)
        self.canvas.pack()
        self.stateString=tk.StringVar(value="Dimensione pennello: 1")
        self.stateLabel=tk.Label(self,textvariable=self.stateString)
        self.stateLabel.pack()
        self.paint_color="black"
        self.brush_radius=1
        self.canvas.bind("<Button-1>",self.onclick_paint)
        self.canvas.bind("<B1-Motion>",self.onclick_paint)
        self.canvas.bind("<Double-Button-1>",self.change_col)
        self.canvas.focus_set()
        self.canvas.bind("<Up>",self.change_brush_size)
        self.canvas.bind("<Down>",self.change_brush_size)
        self.canvas.bind("<c>",self.clear_canvas)
        
         

app=minipaint()


app.mainloop()