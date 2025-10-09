# Pandas — Guida pratica per iniziare (livello base → intermedio)

> Obiettivo: darti gli strumenti essenziali per lavorare con tabelle di dati (CSV/Excel/JSON), analizzarle velocemente e salvare i risultati. Gli esempi sono pensati per l’uso in Jupyter/VS Code o in normali script Python.

---

## 1) Installazione e import
```bash
pip install pandas
```
```python
import pandas as pd
pd.__version__
```

---

## 2) Oggetti fondamentali
- **Series**: colonna monodimensionale con un indice.
- **DataFrame**: tabella 2D (righe × colonne).

```python
s = pd.Series([10, 20, 30], name="valori")
df = pd.DataFrame({
    "nome": ["Anna", "Luca", "Giulia"],
    "eta": [23, 31, 27],
    "citta": ["Roma", "Milano", "Torino"]
})
```

---

## 3) Caricare e salvare dati
### CSV
```python
df = pd.read_csv("file.csv")                     # inferisce il separatore
df = pd.read_csv("file.csv", sep=";")            # se il separatore è ';'
df.to_csv("output.csv", index=False)             # salva senza indice
```
### Excel
```python
df = pd.read_excel("file.xlsx", sheet_name=0)    # o "Foglio1"
df.to_excel("output.xlsx", index=False)
```
### JSON (records/lines)
```python
df = pd.read_json("file.json")                   # struttura tabellare
df.to_json("output.json", orient="records", force_ascii=False, indent=2)
```

> Tip: se un file è grande, usa `nrows=`, `usecols=`, `dtype=`, `chunksize=` per velocizzare.

---

## 4) Ispezione rapida
```python
df.head(3)        # prime 3 righe
df.tail(3)        # ultime 3 righe
df.shape          # (righe, colonne)
df.columns        # nomi colonne
df.dtypes         # tipi di dato per colonna
df.info()         # riepilogo compatto
df.describe(numeric_only=True)   # statistiche numeriche
```

---

## 5) Selezione e filtro
```python
# colonne
df["eta"]                # Series
df[["nome", "citta"]]    # DataFrame

# righe per posizione/indice
df.iloc[0]               # prima riga (Series)
df.iloc[:5]              # prime 5 righe
df.loc[0]                # riga con indice 0 (se l'indice è 0)

# filtro booleano
mask = df["eta"] >= 25
df[mask]

# condizioni multiple
df[(df["eta"] >= 25) & (df["citta"] == "Milano")]
```

> Nota: `loc` usa etichette/indici, `iloc` usa posizioni intere (0-based).

---

## 6) Aggiungere/modificare colonne
```python
df["eta_tra_anni"] = df["eta"] + 5
df["nome_maiuscolo"] = df["nome"].str.upper()

# mappa valori
mappa = {"Roma": "Centro", "Milano": "Nord", "Torino": "Nord"}
df["macroregione"] = df["citta"].map(mappa)

# apply per funzioni più libere (occhio alle performance su dataset grandi)
df["eta_classe"] = df["eta"].apply(lambda x: "under25" if x < 25 else "25+")
```

---

## 7) Valori mancanti (NaN)
```python
df.isna().sum()          # NaN per colonna
df.fillna({"citta": "Sconosciuta"}, inplace=True)   # riempie mancanti
df.dropna(subset=["eta"], inplace=True)             # elimina righe con eta mancante
```

---

## 8) Ordinamento, raggruppamenti, aggregazioni
```python
df.sort_values(by=["eta", "nome"], ascending=[True, True], inplace=False)

# groupby + agg
df.groupby("citta")["eta"].agg(["count", "mean", "min", "max"])

# aggregazioni multiple e su più colonne
df.groupby("citta").agg(
    media_eta=("eta", "mean"),
    n=("nome", "count")
).reset_index()
```

---

## 9) Unire tabelle (merge / join) & concatenare
```python
clienti = pd.DataFrame({
    "id": [1,2,3],
    "nome": ["Anna","Luca","Giulia"]
})
ordini = pd.DataFrame({
    "id_cliente": [1,1,3,3,3],
    "importo": [50, 20, 99, 40, 12]
})

# join chiave-chiave
dfm = clienti.merge(ordini, left_on="id", right_on="id_cliente", how="left")

# concat (stack verticale)
part1 = df.iloc[:2]
part2 = df.iloc[2:]
df_all = pd.concat([part1, part2], ignore_index=True)
```

---

## 10) Pivot e tabelle dinamiche
```python
# pivot: righe→indici, colonne→colonne, values→valore aggregato
df_pivot = pd.pivot_table(
    df, index="citta", columns="eta_classe", values="eta", aggfunc="count", fill_value=0
)
```

---

## 11) Date e tempi (mini intro)
```python
df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
df["anno"] = df["data"].dt.year
df["mese"] = df["data"].dt.month
df["settimana"] = df["data"].dt.isocalendar().week
```

---

## 12) Plot veloce (opzionale)
> Per grafici più curati usa `matplotlib` o `plotly`. Qui un esempio rapidissimo:
```python
df["eta"].plot(kind="hist", bins=10, title="Distribuzione età")
```

---

## 13) Best practice essenziali
- Dai **nomi chiari** alle colonne (snake_case).
- Controlla/converti i **tipi** (`astype`) prima di calcoli.
- Usa **filtri booleani** e **groupby** per analisi veloci.
- Salva output puliti (`to_csv(..., index=False)`).
- Per dataset grandi: specifica `dtype`, usa `chunksize`, evita `apply` dove possibile.

---

# Esercizio base — “Registro studenti”

Ti ho preparato un CSV di partenza: **`studenti.csv`** (allegato qui nella cartella dei file).

## Obiettivo
Caricare il dataset, fare qualche analisi semplice e salvare un paio di risultati.

## Dati (anteprima)
```
Nome,Corso,Voto,Età,Città
Anna,Python,30,23,Roma
Luca,Python,24,31,Milano
Giulia,Django,28,27,Torino
Marco,Python,18,22,Milano
Irene,Django,30,25,Roma
Paolo,Flask,26,29,Roma
Marta,Flask,NaN,24,Milano
```

## Task
1. **Carica** `studenti.csv` in un DataFrame `df`.
2. Stampa **shape**, **dtypes** e **prime 3 righe**.
3. Sostituisci i **voti mancanti** con `0` (solo per la colonna `Voto`).
4. Crea una colonna `Esito` con regola: `Voto >= 18 → "OK"`, altrimenti `"INSUFF"`.
5. Filtra solo gli studenti con `Voto >= 28` e **salva** in `top_studenti.csv` (senza indice).
6. Calcola la **media voto per Corso** (groupby) e ordina **decrescente**.
7. Conta quanti studenti per **Città** e stampa il risultato.
8. (Bonus) Crea un **pivot** con righe=`Città`, colonne=`Corso`, valori=**conteggio** studenti.
9. (Bonus) Ordina il DataFrame originale per `Voto` **decrescente** e salva in `studenti_ordinati.csv`.

> Se vuoi, ti preparo anche una **soluzione** commentata separata.

---

## Mini “cheat sheet” per l’esercizio
```python
import pandas as pd

df = pd.read_csv("studenti.csv")

df.shape, df.dtypes, df.head(3)

df["Voto"] = df["Voto"].fillna(0)
df["Esito"] = df["Voto"].apply(lambda x: "OK" if x >= 18 else "INSUFF")

top = df[df["Voto"] >= 28]
top.to_csv("top_studenti.csv", index=False)

media_per_corso = df.groupby("Corso")["Voto"].mean().sort_values(ascending=False)

conteggio_citta = df["Città"].value_counts()

pivot = pd.pivot_table(df, index="Città", columns="Corso", values="Nome", aggfunc="count", fill_value=0)

df.sort_values(by="Voto", ascending=False).to_csv("studenti_ordinati.csv", index=False)
```