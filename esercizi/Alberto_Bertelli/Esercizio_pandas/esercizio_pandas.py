# # Esercizio Pandas — “Mini vendite negozio” (livello facile)

# ## Obiettivo

# Pulire i dati essenziali e ottenere 3-4 analisi base utili al negozio.

# ## Passi richiesti

# 1. **Carica** il file CSV in un DataFrame `df`. Converte la colonna `Data` in `datetime`.
# 2. Stampa: `shape`, `dtypes`, prime 5 righe.
# 3. **Calcola** una colonna `Ricavo` = `Prezzo * Quantità`.
#     - Gestisci i **valori mancanti**: se `Prezzo` o `Quantità` è NaN, imposta momentaneamente il valore mancante a `0` (solo per il calcolo).
# 4. **Filtra** solo le righe con `Ricavo > 0` in un nuovo DataFrame `df_ok`.
# 5. **Top prodotti**: somma `Ricavo` per `Prodotto` e mostra i **3** prodotti con ricavo totale più alto (ordinati desc).
# 6. **Vendite per Città e Canale** (conteggio ordini): crea una **pivot_table** con righe=`Città`, colonne=`Canale`, valori=conteggio righe (puoi usare `values="Prodotto", aggfunc="count"`), `fill_value=0`, `margins=True`.
# 7. **Ricavo medio per Categoria**: calcola la media di `Ricavo` per `Categoria`, ordinata desc.
# 8. **Salva** due file:
#     - `top_prodotti.csv` con le 3 righe dei prodotti top (colonne: `Prodotto`, `Ricavo_totale`).
#     - `pivot_citta_canale.csv` con la pivot del punto 6 (usa `to_csv`).

## Suggerimenti veloci

# ```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("vendite_negozio.csv", parse_dates=["Data"])

df["Prezzo"] = df["Prezzo"].fillna(0)
df["Quantità"] = df["Quantità"].fillna(0)
df["Ricavo"] = df["Prezzo"] * df["Quantità"]

df_ok = df[df["Ricavo"] > 0]

top_prodotti = (
    df_ok.groupby("Prodotto")["Ricavo"]
         .sum()
         .sort_values(ascending=False)
         .head(3)
         .rename("Ricavo_totale")
         .reset_index()
)

pivot = pd.pivot_table(
    df_ok,
    index="Città",
    columns="Canale",
    values="Prodotto",
    aggfunc="count",
    fill_value=0,
    margins=True, margins_name="Totale"
)

ricavo_medio_cat = (
    df_ok.groupby("Categoria")["Ricavo"]
         .mean()
         .sort_values(ascending=False)
)

top_prodotti.to_csv("top_prodotti.csv", index=False)
pivot.to_csv("pivot_citta_canale.csv")

#Aggiungi una colonna `Mese` estratta da `Data` e calcola il ricavo mensile.
df["Mese"]=df["Data"].dt.month
ricavo_mesile=df.groupby('Mese')["Ricavo"].sum().reset_index()
print(df)
print("\nRicavo mensile:")
print(ricavo_mesile)

#Trova il **giorno** con il ricavo totale più alto

df["Ricavo"]=df["Data"].dt.day
ricavo_mag=df= df["Ricavo"].max()
print(df)
print("\nRicavo maggiore del giorno:")
print(ricavo_mag)


#-   Fai un grafico semplice della distribuzione del `Ricavo` (es. istogramma).

df["Ricavo"].plot()

