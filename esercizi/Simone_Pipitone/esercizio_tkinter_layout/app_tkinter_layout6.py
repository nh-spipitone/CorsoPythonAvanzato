import tkinter as tk
from tkinter import ttk


class TestAppGrid(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Layout with Grid")
        self.geometry("400x300")

        # Configurazione della griglia
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Creazione dei widget
        self.label1 = ttk.Label(self, text="Label 1", background="lightblue")
        self.label2 = ttk.Label(self, text="Label 2", background="lightgreen")
        self.label3 = ttk.Label(self, text="Label 3", background="lightyellow")
        self.label4 = ttk.Label(self, text="Label 4", background="lightpink")

        # Posizionamento dei widget nella griglia
        self.label1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.label2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.label3.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.label4.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.button = ttk.Button(
            self, text="Open New Window", command=self.open_new_window
        )
        self.button.grid(row=2, column=0, columnspan=2, pady=10)

    def open_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("New Window")
        new_window.geometry("200x100")
        ttk.Label(new_window, text="This is a new window").pack(pady=20)


class TestAppPack(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Layout with Pack")
        self.geometry("400x300")

        # Creazione dei widget
        self.label1 = ttk.Label(self, text="Label 1", background="lightblue")
        self.label2 = ttk.Label(self, text="Label 2", background="lightgreen")
        self.label3 = ttk.Label(self, text="Label 3", background="lightyellow")
        self.label4 = ttk.Label(self, text="Label 4", background="lightpink")

        # Posizionamento dei widget con pack
        self.label1.pack(fill="both", expand=True, padx=5, pady=5)
        self.label2.pack(fill="both", expand=True, padx=5, pady=5)
        self.label3.pack(fill="both", expand=True, padx=5, pady=5)
        self.label4.pack(fill="both", expand=True, padx=5, pady=5)
        self.button = ttk.Button(
            self, text="Open New Window", command=self.open_new_window
        )
        self.button.pack(pady=10)

    def open_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("New Window")
        new_window.geometry("200x100")
        ttk.Label(new_window, text="This is a new window").pack(pady=20)


class TestAppPlace(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Layout with Place")
        self.geometry("400x300")

        # Creazione dei widget
        self.label1 = ttk.Label(self, text="Label 1", background="lightblue")
        self.label2 = ttk.Label(self, text="Label 2", background="lightgreen")
        self.label3 = ttk.Label(self, text="Label 3", background="lightyellow")
        self.label4 = ttk.Label(self, text="Label 4", background="lightpink")

        # Posizionamento dei widget con place
        self.label1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.5)
        self.label2.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.5)
        self.label3.place(relx=0.0, rely=0.5, relwidth=0.5, relheight=0.5)
        self.label4.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
        self.button = ttk.Button(
            self, text="Open New Window", command=self.open_new_window
        )
        self.button.place(relx=0.5, rely=0.9, anchor="center")

    def open_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("New Window")
        new_window.geometry("200x100")
        ttk.Label(new_window, text="This is a new window").pack(pady=20)


class TestFrameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Layout with Frames")
        self.geometry("400x300")

        # Creazione dei frame
        self.frame1 = ttk.Frame(self, borderwidth=2, relief="sunken")
        self.frame2 = ttk.Frame(self, borderwidth=2, relief="sunken")

        # Posizionamento dei frame
        self.frame1.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.frame2.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Creazione dei widget nei frame
        self.label1 = ttk.Label(
            self.frame1, text="Label in Frame 1", background="lightblue"
        )
        self.label2 = ttk.Label(
            self.frame2, text="Label in Frame 2", background="lightgreen"
        )

        # Posizionamento dei widget nei frame
        self.label1.pack(fill="both", expand=True, padx=5, pady=5)
        self.label2.pack(fill="both", expand=True, padx=5, pady=5)

        self.button = ttk.Button(
            self, text="Open New Window", command=self.open_new_window
        )
        self.button.pack(pady=10)

    def open_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("New Window")
        new_window.geometry("200x100")
        ttk.Label(new_window, text="This is a new window").pack(pady=20)


app = TestFrameApp()
app.mainloop()
