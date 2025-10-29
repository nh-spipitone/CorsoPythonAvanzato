import tkinter as tk
from tkinter import ttk,messagebox
from pathlib import Path
from PIL import Image, ImageTk
import sqlite3



DB_FILE = "gioco.db"
BGPATH = Path(r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\bg.png")
POKEMONPATHS = [
    Path(r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\treecko.png"),
    Path(r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\torchic.png"),
    Path(r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\mudkip.png"),
]
THUMB_SIZE = (120, 120)



def compose_card(bg_img: Image.Image, char_path: Path | None, size=None) -> Image.Image:
    bg = bg_img.copy().convert("RGBA")
    if size:
        bg = bg.resize(size, Image.Resampling.LANCZOS)
    if char_path and char_path.exists():
        pokemon = Image.open(char_path).convert("RGBA")
        # Always resize pokemon to match bg size
        pokemon = pokemon.resize(bg.size, Image.Resampling.LANCZOS)
        bg = Image.alpha_composite(bg, pokemon)
    return bg


class Pokemon:

    def __init__(self, nome,tipo, hp, attacco):
        self.nome = nome
        self.tipo = tipo
        self.hp = hp
        self.attacco = attacco

    def stato(self):
        return self.hp > 0

    def attacca(self):
        pass

POKEMON = [
    Pokemon("Treecko","Erba", 50, 10),
    Pokemon("Torchic","Fuoco", 45, 12),
    Pokemon("Mudkip","Acqua", 55, 9)
]

class Battaglia_pokemon(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2,weight=1)
        label_seleziona = tk.Label(
            self, text="Seleziona il tuo Pokemon", font=("Times 14")
        )
        btn_battaglia=tk.Button(self,text="Vai alla battaglia",font=("Times 14"))
        btn_battaglia.grid(row=2,column=0,pady=(10,5),sticky="n")
        pokemon_scelto= None

        self.db()
        self.carica_salvataggio()

        label_seleziona.grid(row=0, column=0, pady=(16, 8), sticky="n")
        row = tk.Frame(self)
        row.grid(row=1, column=0, padx=20, pady=12, sticky="nsew")
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(4, weight=1)
        for c in (1, 2, 3):
            row.grid_columnconfigure(c, weight=0)
        row.grid_rowconfigure(0, weight=1)
        bg_full = Image.open(BGPATH)
        bg = bg_full.copy().convert("RGBA")

        bg = bg.resize(THUMB_SIZE, Image.LANCZOS)
        self.bg_tk = ImageTk.PhotoImage(bg)
        for i in range(3):
            btn = tk.Button(
                row,
                image=self.bg_tk,
                bd=0,
                highlightthickness=0,
                cursor="hand2",
                command=lambda idx=i: self.open_preview(idx, bg_full),
            )
            btn.grid(row=0, column=i + 1, padx=12, pady=12)

    def db(self):
        conn=sqlite3.connect(DB_FILE)
        cur=conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scelta (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                tipo TEXT,
                hp INTEGER,
                attacco INTEGER
                )
            """
            )
        conn.commit()
        conn.close()

   

    def open_preview(self, idx, bg):
        if idx < len(POKEMONPATHS):
            pokemon_path = POKEMONPATHS[idx]
            pokemon = POKEMON[idx]
            card = compose_card(bg, pokemon_path, size=(100, 100))
            card_tk = ImageTk.PhotoImage(card)
            top = tk.Toplevel(self)
            top.title("Anteprima Pokemon")
            top.geometry("300x300")
            label = tk.Label(top, image=card_tk)
            label.pack(anchor="center", expand=True)
            top.img_ref = card_tk
            lbl_nome = tk.Label(top, text=pokemon.nome, font=("Arial", 16, "bold"))
            lbl_nome.pack(pady=5)
            lbl_tipo = tk.Label(top, text=f"Tipo: {pokemon.tipo}", font=("Arial", 12))
            lbl_tipo.pack()
            lbl_hp = tk.Label(top, text=f"HP: {pokemon.hp}", font=("Arial", 12))
            lbl_hp.pack(pady=(10,10))
            lbl_attacco = tk.Label(top, text=f"Attacco: {pokemon.attacco}", font=("Arial", 12))
            lbl_attacco.pack(pady=(0,10))
            tk.Button(top,text="Vuoi questo Pokémon ?",font=("Arial", 12, "bold"),command=lambda: self.scegli_pokemon(pokemon, top)).pack(pady=20)


    def scegli_pokemon(self,pokemon,window):
        self.pokemon_scelto=pokemon
        conn= sqlite3.connect(DB_FILE)
        cur=conn.cursor()
        cur.execute("DELETE FROM scelta")
       
        cur.execute("""
            INSERT INTO scelta (id,nome,tipo,hp,attacco)
            VALUES(1, ?, ?, ?, ?)
        """,(pokemon.nome,pokemon.tipo,pokemon.hp,pokemon.attacco))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Secelta effettuata",f"Hai scelto{pokemon.nome}")
        window.destroy()


    def open_battle_preview(self,pokemonEnemy):
        BattleWindow(self,self.pokemon_scelto,pokemonEnemy)
        


    


    def carica_salvataggio(self):
        conn=sqlite3.connect(DB_FILE)
        cur=conn.cursor()
        cur.execute("SELECT nome,tipo,hp,attacco FROM scelta WHERE id=1")
        row = cur.fetchone()
        conn.close()
        if row:
            self.pokemon_scelto=Pokemon(row[0],row[1],row[2],row[3])
            print(f"Pokemon recuperato:{self.pokemon_scelto.nome}")
            
class BattleWindow(tk.Toplevel):
    def __init__(self,master,pokemonPlayer,pokemonEnemy):
        self.title("Battaglia Pokemon")
        if not pokemonPlayer:
            messagebox.showerror("C’è un momento e un luogo per ogni cosa, ma non ora.,Scegli con calma il tuo primo pokemon")
            self.destroy()
        



app = Battaglia_pokemon()
app.mainloop()
