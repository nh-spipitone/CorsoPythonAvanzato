import tkinter as tk

root = tk.Tk()
root.title("Eventi Tkinter")

status = tk.StringVar(value="Clicca sul box")

box = tk.Label(root, text="Box", bg="lightgray", width=20, height=10)
box.pack(padx=10, pady=10, fill="x")
tk.Label(root, textvariable=status).pack(pady=5)


def on_click(event):
    status.set(f"Box cliccato! x: {event.x}, y: {event.y}")


def on_double_click(event):
    status.set("Reset")
    box.config(bg="lightgray")


def on_enter(event):
    box.config(bg="lightblue")


def on_leave(event):
    box.config(bg="lightgray")


box.bind("<Button-1>", on_click)
box.bind("<Double-Button-1>", on_double_click)
box.bind("<Enter>", on_enter)
box.bind("<Leave>", on_leave)

root.mainloop()
