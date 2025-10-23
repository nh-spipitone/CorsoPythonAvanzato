import tkinter as tk
from tkinter import ttk,messagebox

root =tk.Tk()
root.title("Stopwatch")


timer_attivo = False
var_mseconds =tk.IntVar(value=0)
var_second =tk.IntVar(value=0)
job=None
label1=ttk.Label(root,font=("Arial", 16)).pack(pady=20)
lista=tk.Listbox(root,height=6)
lista.pack(padx=10, pady=(6, 12), fill="x")



def start():
    global timer_attivo
    if not timer_attivo:
        timer_attivo= True
        update_timer()


def update_timer():
    global timer_attivo ,var_mseconds,job,var_second,label1
    if timer_attivo:
        msecond = var_mseconds.get()
        second = var_second.get()
        if msecond<60:
            var_mseconds.set(msecond+1)
        else:
            var_mseconds.set(0)
            var_mseconds= second+1
    job=root.after(100,update_timer)
    label1.config(text=f"{second+1:02d}:{msecond+1:02d}")

def stop():
    global timer_attivo,job
    timer_attivo = False
    root.after_cancel(job)
    messagebox.showinfo("Cronometro stoppato")

def reset():
    global timer_attivo,job,var_mseconds,var_second,lista,label1
    timer_attivo = False
    if job:
        root.after_cancel(job)
    label1.config(text="00:00")
    var_mseconds.set(0)
    var_second.set(0)
    lista.delete(0,"end")

def lap():
    global var_mseconds, var_second,lista
    secondi = var_second.get()
    milsec = var_mseconds.get()
    lista.insert("end",f"{secondi:02d}:{milsec:02d}")


ttk.Button(root, text="Start", command=start).pack(pady=10)
ttk.Button(root, text="Stop", command=stop).pack(pady=10)
ttk.Button(root, text="Reset", command=reset).pack(pady=10)
ttk.Button(root, text="Lap", command=lap).pack(pady=10)        

root.mainloop()