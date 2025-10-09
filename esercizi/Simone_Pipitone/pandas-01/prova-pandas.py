import pandas as pd

df = pd.DataFrame(
    {
        "nome": ["Anna", "Luca", "Giulia", "Marco", "Paola", "Giovanni"],
        "eta": [23, 31, 27, 16, None, 45],
        "citta": ["Roma", "Milano", "Torino", "Napoli", None, "Milano"],
    }
)

# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.dtypes)
# print(df.info())
# print(df.describe())


# print(df["eta"])
# print(df[["nome", "citta"]])


# print(df.iloc[0])  # prima riga
# print("-" * 30)  # separatore

# print(df.iloc[:5])  # prime 5 righe
# print("-" * 30)  # separatore

# print(df.loc[0])  # prima riga
# print("-" * 30)  # separatore

# print(df.iloc[:, 0])  # prima colonna
# print("-" * 30)  # separatore

# mask = df["eta"] > 25

# print(df[mask])  # righe con eta > 25

# print(df[(df["eta"] >= 25) & (df["citta"] == "Milano")])

# df["eta_10"] = df["eta"] + 10
# print(df)
# df["nome_minuscolo"] = df["nome"].str.lower()
# print(df)


# def is_adult(age):

#     return age >= 18


# df["is_adult"] = df["eta"].apply(is_adult)
# print(df)

# mappa = {"Roma": "Centro", "Milano": "Nord", "Torino": "Nord"}
# df["macroregione"] = df["citta"].map(mappa)
# print(df)


# print(df.isna().sum())

# df.fillna({"citta": "Sconosciuta"}, inplace=True)
# print(df)

df.dropna(subset=["eta"], inplace=True)

# print(df)


df.sort_values(by=["eta", "nome"], ascending=[True, False], inplace=False)
df.sort_values(by=["eta"], ascending=[False], inplace=True)


df.groupby("citta")["eta"].agg(["count", "mean", "min", "max"])


print(df.groupby("citta")["eta"].agg(["count", "mean", "min", "max"]))
