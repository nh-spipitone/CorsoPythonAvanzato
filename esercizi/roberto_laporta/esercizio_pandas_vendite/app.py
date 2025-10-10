import pandas as pd
import matplotlib.pyplot as plt

PATH_CSV="vendite_negozio.csv"
PATH_CSV_TOP_PRODUCTS='top_prodotti.csv'
PATH_CSV_PIVOT='pivot_citta_canale.csv'

#1
df = pd.read_csv(PATH_CSV)
df["Data"] = pd.to_datetime(df["Data"])

#2
first_five = df.head()
# print(first_five.shape)
# print(first_five.dtypes)

#3
df['Ricavo'] = df['Prezzo'].fillna(0) * df['Quantità'].fillna(0)

#4
filter_no_ravenue = df['Ricavo'] == 0
df_ok = df[filter_no_ravenue]

#5
calc_ravenue_product = df.groupby("Prodotto")["Ricavo"].sum()
ordered_products = calc_ravenue_product.sort_values(ascending=False)
df_top_3 = ordered_products.head(3)

#6
df_pivot = pd.pivot_table(
    df, index="Città", columns="Canale", values="Prodotto", aggfunc="count", fill_value=0, margins=True
)

#7
df_mean_category = df.groupby("Categoria")["Ricavo"].mean()

#8
df_top_products= df_top_3.reset_index()
df_top_products.columns = ['Prodotto', 'Ricavo_totale']
df_top_products.to_csv(PATH_CSV_TOP_PRODUCTS, index=False)

df_pivot.to_csv(PATH_CSV_PIVOT)

# extra 1
df['Mese'] = df['Data'].dt.month
df_month_ravenue =  df.groupby("Mese")["Ricavo"].mean()

# extra 2
df_day_ravenue = df.groupby('Data')['Ricavo'].sum()
day_max_ravenue = df_day_ravenue.idxmax()

# extra 3
hist = df["Ricavo"].hist(bins=5)
plt.show()