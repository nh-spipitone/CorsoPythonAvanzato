import pandas as pd

"""
Operazioni su DataFrame pandas e esempi di manipolazione dati.

Questo script dimostra varie operazioni pandas tra cui:
- Creazione di DataFrame ed esplorazione di base (head, shape, columns, dtypes, info, describe)
- Selezione dei dati usando nomi di colonne, iloc e loc
- Maschere booleane e filtri
- Aggiunta di nuove colonne con calcoli e trasformazioni
- Applicazione di funzioni alle colonne
- Mappatura di valori per creare nuove colonne
- Gestione dei valori mancanti (isna, fillna, dropna)
- Ordinamento dei dati
- Raggruppamento e aggregazione
- Unione di DataFrame (merge)
- Concatenazione di DataFrame
- Suddivisione di dati continui in intervalli con pd.cut
- Creazione di tabelle pivot

La funzione pd.cut() viene utilizzata per suddividere dati numerici continui in intervalli discreti.
In questo esempio:
- df["eta"] contiene le età da suddividere in classi
- bins=[0, 20, 30, 50] definisce i bordi degli intervalli (0-20, 21-30, 31-50)
- labels=["0-20", "21-30", "31-50"] assegna etichette personalizzate a ciascun intervallo
- Il risultato crea una nuova colonna categorica "eta_classe" che classifica ogni età nell'intervallo corrispondente

La tabella pivot alla fine crea una tabulazione incrociata che mostra il conteggio delle persone 
per città (indice) e classe di età (colonne).
"""

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


# df.sort_values(by=["eta", "nome"], ascending=[True, False], inplace=False)
# df.sort_values(by=["eta"], ascending=[False], inplace=True)


# df.groupby("citta")["eta"].agg(["count", "mean", "min", "max"])


# print(df.groupby("citta")["eta"].agg(["count", "mean", "min", "max"]))

# print(
#     df.groupby("citta")
#     .agg(media_eta=("eta", "mean"), n=("nome", "count"))
#     .reset_index()
# )

# clienti = pd.DataFrame({"id": [1, 2, 3], "nome": ["Anna", "Luca", "Giulia"]})
# ordini = pd.DataFrame({"id_cliente": [1, 1, 3, 3, 3], "importo": [50, 20, 99, 40, 12]})

# # join chiave-chiave
# dfm = clienti.merge(ordini, left_on="id", right_on="id_cliente", how="left")

# print(dfm)

# concat (stack verticale)
# part1 = df.iloc[:2]
# print(part1)
# part2 = df.iloc[2:]
# print(part2)
# df_all = pd.concat([part1, part2], ignore_index=True)
# print(df_all)

df["eta_classe"] = pd.cut(
    df["eta"], bins=[0, 20, 30, 50], labels=["0-20", "21-30", "31-50"]
)

print(df["eta_classe"])

# pivot: righe→indici, colonne→colonne, values→valore aggregato
df_pivot = pd.pivot_table(
    df, index="citta", columns="eta_classe", values="eta", aggfunc="count", fill_value=0
)
print(df_pivot)

df["data"] = ["2023/01/15", "2022/12/30", "2023/03/22", "2023/07/11", "2023/05/05"]

# Converte la colonna "data" in formato datetime, interpretando il primo giorno del mese (formato europeo)
# errors="coerce" imposta NaT (Not a Time) per valori non validi
# Esempio 1: Conversione con formato europeo (giorno/mese/anno)
df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
print("Formato europeo:")
print(df["data"])

# Esempio 2: Conversione con formato specificato esplicitamente
df["data_custom"] = pd.to_datetime(df["data"], format="%Y/%m/%d", errors="coerce")
print("\nFormato personalizzato (YYYY/MM/DD):")
print(df["data_custom"])

# Esempio 3: Conversione da timestamp Unix
df["timestamp"] = [1673740800, 1672358400, 1679443200, 1689033600, 1683244800]
df["data_from_timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
print("\nDa timestamp Unix:")
print(df["data_from_timestamp"])

# Esempio 4: Formattazione output come stringa
df["data_formattata"] = df["data"].dt.strftime("%d/%m/%Y")
print("\nData formattata (gg/mm/aaaa):")
print(df["data_formattata"])

# Esempio 5: Altri formati di output
df["data_completa"] = df["data"].dt.strftime(
    "%A %d %B %Y"
)  # es: Monday 15 January 2023
df["data_iso"] = df["data"].dt.strftime("%Y-%m-%d")  # formato ISO
df["data_ora"] = df["data"].dt.strftime("%d/%m/%Y %H:%M:%S")  # con ora
print("\nVari formati di output:")
print(df[["data_completa", "data_iso", "data_ora"]])

# Estrae l'anno dalla colonna datetime e lo salva in una nuova colonna "anno"
df["anno"] = df["data"].dt.year

# Estrae il mese (1-12) dalla colonna datetime e lo salva in una nuova colonna "mese"
df["mese"] = df["data"].dt.month

# Estrae il numero della settimana ISO (1-53) e lo salva in una nuova colonna "settimana"
df["settimana"] = df["data"].dt.isocalendar().week

print(df)

# Crea un istogramma della colonna "eta" con 10 intervalli (bins) e titolo "Distribuzione età"

a = df["eta"].plot(kind="hist", bins=10, title="Distribuzione età")
a.figure.savefig("eta_hist.png")
