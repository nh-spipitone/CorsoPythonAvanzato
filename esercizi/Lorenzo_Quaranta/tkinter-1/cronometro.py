import tkinter as tk
from tkinter import ttk,messagebox

class cronometro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stopwatch")
        self.geometry("640x480")
        self.tenths=tk.IntVar(value=0)
        self.seconds=tk.IntVar(value=0)
        self.minutes=tk.IntVar(value=0)
        self.job=None
        self.running=False
        empty_list=[]
        self.laps=tk.Variable(value=empty_list)
        self.lapbox=tk.Listbox(self,listvariable=self.laps).pack()


        self.timer_txt=tk.StringVar(value="00:00.0")
        self.timer=tk.Label(self,textvariable=self.timer_txt,font=("Helvetica", 48)).pack()
        self.buttonStart=tk.Button(self,text="inizia",command=self.start_timer).pack()
        self.buttonStop=tk.Button(self,text="stop",command=self.stop_timer).pack()
        self.buttonReset=tk.Button(self,text="reset",command=self.reset).pack()
        self.buttonLap=tk.Button(self,text="lap",command=self.add_to_laps).pack()
        
    def start_timer(self):
            if not self.running:
                  self.running=True
                  self.update_timer()
    
    def stop_timer(self):
         if self.running:
            self.running=False
        
    def update_timer(self):
            if self.running:
                t=self.tenths.get()
                s=self.seconds.get()
                m=self.minutes.get()
                if t<9:
                    self.tenths.set(t+1)
                elif s<59:
                    self.tenths.set(0)
                    self.seconds.set(s+1)
                else:
                    self.tenths.set(0)
                    self.seconds.set(0)
                    self.minutes.set(m+1)
                seconds_string="0"+str(s) if s<9 else str(s)
                minutes_string="0"+str(m) if m<9 else str(m)
                self.job=self.after(100,self.update_timer)
                self.timer_txt.set(minutes_string+":"+seconds_string+"."+str(t))
                
                
            

    def reset(self):
            self.running=False
            self.tenths.set(0)
            self.seconds.set(0)
            self.minutes.set(0)
            self.timer_txt.set("00:00.0")
            empty_list=[]
            self.laps.set(empty_list)
            self.after_cancel(self.job)

    def add_to_laps(self):
        time=self.timer_txt.get().strip()
        laps_list=self.laps.get()
        laps_list.append(time)
        self.laps.set(laps_list)



if __name__=="__main__":
   app= cronometro() 
   app.mainloop()