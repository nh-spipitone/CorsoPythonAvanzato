import pandas
df_negozio=pandas.read_csv("vendite_negozio.csv")

df_negozio["Data"]=pandas.to_datetime(df_negozio["Data"],dayfirst=True,errors="coerce")

print(df_negozio.shape)

print(df_negozio.dtypes)

print(df_negozio[:5])
df_negozio["Prezzo"]=df_negozio["Prezzo"].fillna(0)
df_negozio["Quantità"]=df_negozio["Quantità"].fillna(0)
df_negozio["Ricavo"]=df_negozio["Prezzo"]*df_negozio["Quantità"]
print("-" * 30) 
print(df_negozio)

df_ok=df_negozio[df_negozio["Ricavo"]>0]
print("-" * 30) 
print(df_ok)
top_prodotti = (
    df_ok.groupby("Prodotto")["Ricavo"]
         .sum()
         .sort_values(ascending=False)
         .head(3)
         .rename("Ricavo_totale")
         .reset_index()
)
print("-" * 30) 
print(top_prodotti)


vendite_filtrate=pandas.pivot_table(df_negozio,index="Città",columns="Canale",values="Prodotto",aggfunc="count",fill_value=0,margins=True)

print("-" * 30) 
print(vendite_filtrate)

ricavo_per_cat=(
    df_ok.groupby("Categoria")["Ricavo"]
         .mean()
         .sort_values(ascending=False)
         .rename("Ricavo_medio")
         .reset_index()
)

print("-" * 30) 
print(ricavo_per_cat)

top_prodotti.to_csv("top_prodotti.csv",index=False)
vendite_filtrate.to_csv("pivot_citta_canale.csv",index=False)