import tkinter as tk
from tkinter import ttk,messagebox

class cronometro(tk.Tk):
    def __init__(self):
        self.title("Stopwatch")
        self.tenths=tk.IntVar(value=0)
        self.seconds=tk.IntVar(value=0)
        self.minutes=tk.IntVar(value=0)
        self.job=None
        self.running=False
        self.start_time=None
        self.accum=0
        self.lapbox=tk.Listbox(self)


        self.timer_txt=tk.StringVar(value="00:00.0")
        self.timer=tk.Label(self,textvariable=self.timer_txt,font=("Helvetica", 48)).pack()
        self.buttonStart=tk.Button(self,text="inizia").pack()
        self.buttonStop=tk.Button(self,text="stop").pack()
        self.buttonReset=tk.Button(self,text="reset").pack()
        def lap(self):
            pass
        
        def reset(self):
            pass

        def after_cancel(self):
            pass