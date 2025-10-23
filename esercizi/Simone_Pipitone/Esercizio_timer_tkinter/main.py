import tkinter
import tkinter.messagebox as messagebox


class TimerApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timer Tkinter")
        self.seconds = tkinter.IntVar(value=10)
        self.running = False
        self.job = None

        self.label = tkinter.Label(self, text="00:00", font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.start_button = tkinter.Button(
            self, text="Start Timer", command=self.start_timer
        )
        self.start_button.pack(pady=10)

        self.reset_button = tkinter.Button(
            self, text="Reset Timer", command=self.reset_timer
        )
        self.reset_button.pack(pady=10)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def reset_timer(self):
        self.running = False
        self.label.config(text="00:00")
        if self.job:
            self.after_cancel(self.job)
        self.seconds.set(10)

    def update_timer(self):
        if self.running:
            s = self.seconds.get()
            if s > 0:
                self.seconds.set(s - 1)
                self.job = self.after(1000, self.update_timer)
                self.label.config(text=f"00:{s-1:02d}")

            else:
                self.running = False
                messagebox.showinfo("Timer", "Tempo scaduto!")


app = TimerApp()
app.mainloop()
