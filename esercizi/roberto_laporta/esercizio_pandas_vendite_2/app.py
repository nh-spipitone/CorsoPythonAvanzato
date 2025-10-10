import pandas as pd

# Creazione del DataFrame con dati forniti
data = {
'ID_Transazione': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
'Cliente': ['Cliente1', 'Cliente2', 'Cliente3', 'Cliente4', 'Cliente5',
'Cliente6', 'Cliente7', 'Cliente8', 'Cliente9', 'Cliente10'],
'Prodotto': ['Prodotto1', 'Prodotto2', 'Prodotto3', 'Prodotto1', 'Prodotto2',
'Prodotto3', 'Prodotto1', 'Prodotto2', 'Prodotto3', 'Prodotto1'],
'Quantità': [3, 5, 2, 4, 1, 3, 4, 5, 2, 3],
'Prezzo': [15.5, 23.2, 10.0, 20.0, 18.5, 12.7, 17.0, 22.5, 14.5, 19.0]
}

df = pd.DataFrame(data)

#1
product_quantity_sum = df.groupby("Prodotto")["Quantità"].sum()
sorted_product_quantity_sum = product_quantity_sum.sort_values(ascending=False)

top_3 = sorted_product_quantity_sum.head(3)

#2
df['Ricavo'] = df['Quantità'] * df['Prezzo']
ravenue_for_customer = df.groupby('Cliente')['Ricavo'].sum()
sorted_ravenue_for_customer = ravenue_for_customer.sort_values(ascending=False)

top_customer = sorted_ravenue_for_customer.head(1)

#3
index_max_ravenue = df['Ricavo'].idxmax()
transation_max_ravenue = df.loc[index_max_ravenue]

top_product = transation_max_ravenue['Prodotto']
top_customer = transation_max_ravenue['Cliente']
max_ravenue = transation_max_ravenue['Ricavo']

print(top_product)
print(top_customer)
print(max_ravenue)