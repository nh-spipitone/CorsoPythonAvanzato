import pandas as pd

# 1 leggi CSV
df = pd.read_csv(r"esercizi\Simone_Pipitone\esercizio-pandas-01\studenti.csv")

# 2 stampa shape,dtypes,head(3)
print(df.shape)
print(df.dtypes)
print(df.head(3), "\n")
# 3
df["Voto"] = df["Voto"].fillna(0)


# 4
def checkesito(voto):
    if voto >= 18:
        return "OK"
    else:
        return "INSUFF"


df["Esito"] = df["Voto"].apply(checkesito)

# 5
df2 = df[df["Voto"] >= 28]
df2.to_csv(
    r"esercizi\Simone_Pipitone\esercizio-pandas-01\top_studenti.csv", index=False
)
# 6

media_voto_per_corso = df.groupby("Corso")["Voto"].mean().sort_values(ascending=False)

# 7
conteggio_citta = df["Città"].value_counts()

# 8
pivot = pd.pivot_table(
    df, index="Città", columns="Corso", values="Nome", aggfunc="count", fill_value=0
)
print(pivot)

# 9

df_ordinato = df.sort_values(by="Voto", ascending=False)
df_ordinato.to_csv(
    r"esercizi\Simone_Pipitone\esercizio-pandas-01\studenti_ordinati.csv", index=False
)
print(df_ordinato)
