import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import sqlite3
from pydantic import BaseModel
from typing import List, Literal
import random


DB_FILE = "gioco.db"
BGPATH = Path(
    r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\bg.png"
)
POKEMONPATHS = [
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\treecko.png"
    ),
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\torchic.png"
    ),
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\mudkip.png"
    ),
]

POKEMONBACKPATHS = [
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\treecko_back.png"
    ),
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\torchic_back.png"
    ),
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\mudkip_back.png"
    ),
]

POKEMONENEMYPATHS = [
    Path(
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\poochyena.png"
    ),
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


class Mossa(BaseModel):
    nome: str
    potenza: int
    precisione: int
    tipo: Literal["Erba", "Fuoco", "Acqua", "Buio", "Normale"]


class Pokemon:

    def __init__(
        self, nome, livello, tipo, hp, attacco, sprite, back_sprite, mosse: list[Mossa]
    ):
        self.nome = nome
        self.livello = livello
        self.tipo = tipo
        self.hp = hp
        self.max_hp = hp
        self.attacco = attacco
        self.sprite = sprite
        self.back_sprite = back_sprite
        self.mosse = mosse

    def stato(self):
        return self.hp > 0

    def attacca(self, nemico, idx):

        potenza = self.mosse[idx].potenza
        danno = self.attacco * (potenza / 100)
        seed = random.randint(0, 100)
        if seed <= self.mosse[idx].precisione:

            nemico.hp -= danno
            return True

        return False


mosse_treecko = [
    Mossa(nome="Colpo Basso", potenza=10, precisione=70, tipo="Erba"),
    Mossa(nome="Frustata", potenza=14, precisione=95, tipo="Erba"),
]
mosse_torchic = [
    Mossa(nome="Braciere", potenza=15, precisione=85, tipo="Fuoco"),
    Mossa(nome="Graffio", potenza=10, precisione=90, tipo="Normale"),
]

mosse_mudkip = [
    Mossa(nome="Pistolacqua", potenza=13, precisione=80, tipo="Acqua"),
    Mossa(nome="Botta", potenza=10, precisione=75, tipo="Normale"),
]

POKEMON = [
    Pokemon(
        "Treecko",
        5,
        "Erba",
        50,
        10,
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\treecko.png",
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\treecko_back.png",
        mosse_treecko,
    ),
    Pokemon(
        "Torchic",
        5,
        "Fuoco",
        45,
        12,
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\torchic.png",
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\torchic_back.png",
        mosse_torchic,
    ),
    Pokemon(
        "Mudkip",
        5,
        "Acqua",
        55,
        9,
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\mudkip.png",
        r"CorsoPythonAvanzato\esercizi\Alberto_Bertelli\esercizio-finale\immagini\mudkip_back.png",
        mosse_mudkip,
    ),
]

attacchi_poochyena = [
    Mossa(nome="Morso", potenza=11, precisione=70, tipo="Buio"),
    Mossa(nome="Graffio", potenza=10, precisione=90, tipo="Normale"),
    Mossa(nome="Zanna", potenza=12, precisione=80, tipo="Buio"),
    Mossa(nome="Furia", potenza=14, precisione=75, tipo="Normale"),
]


class Battaglia_pokemon(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        label_seleziona = tk.Label(
            self, text="Seleziona il tuo Pokemon", font=("Times 14")
        )
        btn_battaglia = tk.Button(
            self,
            text="Vai alla battaglia",
            font=("Times 14"),
            command=lambda: self.open_battle_preview(
                Pokemon(
                    "Poochyena",
                    4,
                    "Buio",
                    48,
                    11,
                    str(POKEMONENEMYPATHS[0]),
                    "",
                    mosse=attacchi_poochyena,
                )
            ),
        )
        btn_battaglia.grid(row=2, column=0, pady=(10, 5), sticky="n")
        pokemon_scelto = None

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
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        # Aggiungi la colonna mosse se non esiste
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scelta (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                livello INTEGER,    
                tipo TEXT,
                hp INTEGER,
                attacco INTEGER,
                sprite TEXT,
                back_sprite TEXT,
                mosse TEXT
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
            lbl_hp.pack(pady=(10, 10))
            lbl_attacco = tk.Label(
                top, text=f"Attacco: {pokemon.attacco}", font=("Arial", 12)
            )
            lbl_attacco.pack(pady=(0, 10))
            tk.Button(
                top,
                text="Vuoi questo Pokémon ?",
                font=("Arial", 12, "bold"),
                command=lambda: self.scegli_pokemon(pokemon, top),
            ).pack(pady=20)

    def scegli_pokemon(self, pokemon, window):
        import json

        self.pokemon_scelto = pokemon
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM scelta")

        mosse_json = json.dumps([m.dict() for m in pokemon.mosse])
        cur.execute(
            """
            INSERT INTO scelta (id,nome,livello,tipo,hp,attacco,sprite,back_sprite,mosse)
            VALUES(1, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                pokemon.nome,
                pokemon.livello,
                pokemon.tipo,
                pokemon.hp,
                pokemon.attacco,
                pokemon.sprite,
                pokemon.back_sprite,
                mosse_json,
            ),
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Secelta effettuata", f"Hai scelto{pokemon.nome}")
        self.carica_salvataggio()
        window.destroy()

    def open_battle_preview(self, pokemonEnemy):
        BattleWindow(self, self.pokemon_scelto, pokemonEnemy)

    def carica_salvataggio(self):
        import json

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(
            "SELECT nome,livello,tipo,hp,attacco,sprite,back_sprite,mosse FROM scelta WHERE id=1"
        )
        row = cur.fetchone()
        conn.close()
        if row:
            mosse = []
            if row[7]:
                try:
                    mosse = [Mossa(**m) for m in json.loads(row[7])]
                except Exception:
                    mosse = []
            self.pokemon_scelto = Pokemon(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], mosse
            )
            print(f"Pokemon recuperato:{self.pokemon_scelto.nome}")


class BattleWindow(tk.Toplevel):
    def __init__(self, master, pokemonPlayer, pokemonEnemy):
        super().__init__(master)
        self.title("Battaglia Pokemon")
        self.resizable(False, False)
        self._img_cache = []
        self.configure(bg="#1b1d23")
        if not pokemonPlayer:
            messagebox.showerror(
                "C’è un momento e un luogo per ogni cosa, ma non ora.,Scegli con calma il tuo primo pokemon"
            )
            self.destroy()
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Battle.TFrame", background="#1b1d23")
        style.configure("Text.TLabel", background="#0e1116", foreground="#ffffff")
        style.configure("Info.TLabel", background="#2b2f3a", foreground="#ffffff")
        style.configure("InfoValue.TLabel", background="#2b2f3a", foreground="#c7ffd1")
        style.configure(
            "HP.Horizontal.TProgressbar",
            thickness=12,
            background="#4caf50",
            troughcolor="#2b2f3a",
        )
        style.map("TButton", focuscolor=[("!focus", "#000000")])

        main = ttk.Frame(self, padding=12, style="Battle.TFrame")
        main.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(
            main, width=640, height=360, bg="#6fb3ff", highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Piattaforme (ellissi prato)
        self.canvas.create_oval(420, 130, 600, 170, fill="#e8f7f0", outline="")
        self.canvas.create_oval(80, 260, 300, 310, fill="#dff3ea", outline="")

        enemy_info = self._make_info_frame(main, pokemonEnemy.__dict__)
        player_info = self._make_info_frame(main, pokemonPlayer.__dict__)
        self.canvas.create_window(20, 20, anchor="nw", window=enemy_info)  # top-left
        self.canvas.create_window(
            340, 220, anchor="nw", window=player_info
        )  # bottom-right
        self.place_sprite(self.canvas, pokemonPlayer.back_sprite, 200, 260)
        self.place_sprite(self.canvas, pokemonEnemy.sprite, 500, 120)
        self.btn_attacca = tk.Button(
            self,
            text="ATTACCA",
            font=("Arial", 14, "bold"),
            bg="#ff5050",
            fg="white",
            command=lambda: enemy_info.set_hp(enemy_info.hp_var.get() - 10),
        )
        self.btn_attacca.grid(row=1, column=0, pady=20)

    def _make_info_frame(self, parent, mon: dict) -> ttk.Frame:
        """Mini pannello con Nome/Lv + HP bar + HP numerici."""
        f = ttk.Frame(parent, style="Battle.TFrame")  # contenitore invisibile
        box = ttk.Frame(f, style="Battle.TFrame")
        box.grid(row=0, column=0)

        # Sfondo scuro del riquadro info
        bg = tk.Frame(box, bg="#2b2f3a")
        bg.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        name = mon.get("nome", "???")
        level = mon.get("livello", 5)
        hp = int(mon.get("hp", 1))
        max_hp = max(1, int(mon.get("max_hp", 1)))

        top = ttk.Frame(bg, style="Battle.TFrame")
        top.pack(fill="x", padx=8, pady=(8, 4))
        lbl_name = ttk.Label(top, text=f"{name}   Lv.{level}", style="Info.TLabel")
        lbl_name.pack(side="left")

        bar_frame = ttk.Frame(bg, style="Battle.TFrame")
        bar_frame.pack(fill="x", padx=8, pady=(0, 6))

        f.hp_var = tk.IntVar(value=min(hp, max_hp))
        f.hp_txt = tk.StringVar(value=f"{hp}/{max_hp}")

        f.hpbar = ttk.Progressbar(
            bar_frame,
            style="HP.Horizontal.TProgressbar",
            maximum=max_hp,
            variable=f.hp_var,
            length=220,
            mode="determinate",
        )
        f.hpbar.pack(side="left", padx=(0, 8))

        f.lbl_val = ttk.Label(
            bar_frame, textvariable=f.hp_txt, style="InfoValue.TLabel"
        )
        f.lbl_val.pack(side="left")

        def set_hp(new_hp: int, new_max: int | None = None):
            if new_max is not None:
                f.hpbar.configure(maximum=new_max)
            maxv = int(f.hpbar.cget("maximum"))
            clamped = max(0, min(int(new_hp), maxv))
            f.hp_var.set(clamped)
            f.hp_txt.set(f"{clamped}/{maxv}")

        f.set_hp = set_hp

        return f

    def place_sprite(self, canvas, path, x, y):
        image = None
        if path:
            image = tk.PhotoImage(file=Path(path))
            self._img_cache.append(image)
        if image:
            canvas.create_image(x, y, image=image)


app = Battaglia_pokemon()
app.mainloop()
