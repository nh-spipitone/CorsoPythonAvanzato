import pandas as pd
import matplotlib.pyplot as plt

# 1
df = pd.read_csv(
    r"esercizi/Elisa_Genesio/es_3/vendite_negozio.csv", parse_dates=["Data"]
)

# 2
print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nPrime 5 righe:\n", df.head())

# 3
df["Prezzo"] = df["Prezzo"].fillna(0)
df["Quantità"] = df["Quantità"].fillna(0)
df["Ricavo"] = df["Prezzo"] * df["Quantità"]

# 4
df_ok = df[df["Ricavo"] > 0]

# 5
top_prodotti = (
    df_ok.groupby("Prodotto")["Ricavo"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .rename("Ricavo_totale")
    .reset_index()
)
print("\nTop 3 prodotti:\n", top_prodotti)

# 6
pivot = pd.pivot_table(
    df_ok,
    index="Città",
    columns="Canale",
    values="Prodotto",
    aggfunc="count",
    fill_value=0,
    margins=True,
    margins_name="Totale",
)
print("\nPivot Città-Canale:\n", pivot)

# 7
ricavo_medio_cat = (
    df_ok.groupby("Categoria")["Ricavo"].mean().sort_values(ascending=False)
)
print("\nRicavo medio per Categoria:\n", ricavo_medio_cat)

# 8
top_prodotti.to_csv(r"esercizi/Elisa_Genesio/es_3/top_prodotti.csv", index=False)
pivot.to_csv(r"esercizi/Elisa_Genesio/es_3/pivot_citta_canale.csv")

# Aggiungi colonna Mese
df_ok["Mese"] = df_ok["Data"].dt.to_period("M").astype(str)

# Ricavo mensile
ricavo_mensile = df_ok.groupby("Mese")["Ricavo"].sum()
print("\nRicavo mensile:\n", ricavo_mensile)

# Giorno con ricavo più alto
giorno_top = df_ok.groupby("Data")["Ricavo"].sum().idxmax()
print("\nGiorno con il ricavo più alto:", giorno_top)

# Grafico
plt.figure(figsize=(8, 4))
plt.hist(df_ok["Ricavo"], bins=30)
plt.title("Distribuzione del Ricavo")
plt.xlabel("Ricavo")
plt.ylabel("Frequenza")
plt.savefig(r"esercizi/Elisa_Genesio/es_3/vendite_grafico")

# Risultato
print("\n", df)
print("\n", df_ok)
