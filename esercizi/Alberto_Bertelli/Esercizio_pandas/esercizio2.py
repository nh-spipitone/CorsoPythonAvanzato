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

# Creazione del DataFrame
df = pd.DataFrame(data)

# 1. Esplorazione del DataFrame
print(df.head(5))
print(df.isnull().sum())



# 2. Creazione della colonna 'Totale'
df['Totale'] = df['Quantità'] * df['Prezzo']

# 3. Filtraggio per Quantità > 3
df_filtrato = df[df['Quantità'] > 3]

# 4. Raggruppamento per Prodotto
vendite_per_prodotto = df.groupby('Prodotto')['Totale'].sum()

# 5. Ordinamento del DataFrame per 'Totale'
df_ordinato = df.sort_values(by='Totale')

#6 Raggruppa i dati per Prodotto e calcola la somma delle quantità vendute.
quantita_vendute = df.groupby("Prodotto")["Quantità"].sum()


##7 Ordina i risultati in ordine decrescente per quantità.
df_ordinato_dec = df.sort_values(by='Quantità', ascending=False)

#8 Mostra solo i primi 3 prodotti più venduti.
df_prodotti_ven=quantita_vendute.sort_values(ascending=False).head(3) #ascending fa fare l'ordinamento se metti False farà in maniera decrescente


##9 Raggruppa i dati per Cliente e calcola la somma totale delle vendite per ciascun cliente.
df_ordine_cliente= df.groupby("Cliente")["Totale"].sum()

#10 Ordina i risultati in ordine decrescente per somma totale.
df_ordinato_cliente = df_ordine_cliente.sort_values(ascending=False)

#11 Mostra il cliente che ha speso di più.
sf_spendaccione = df_ordinato_cliente.head(1)

##12 Calcola il totale per ogni transazione (è già presente nel DataFrame come Totale).
totale_complessivo =df["Totale"].sum()
#13 Trova il prodotto con il maggior guadagno in un singolo acquisto (individuato dal massimo valore nella colonna Totale).


# Visualizzazione dei risultati finali
print("\nVendite per Prodotto:")
print(vendite_per_prodotto)
print("\nDataFrame Ordinato:")
print(df_ordinato)
print(quantita_vendute)
print(df_ordinato_dec)
print(df_prodotti_ven)
print(df_ordine_cliente)
print("\ndf_ordinato_cliente:")
print(df_ordinato_cliente)
print("\nsf_spendaccione:")
print(sf_spendaccione)
print(totale_complessivo)


# 1. Trova la transazione con il guadagno massimo
max_guadagno = df.loc[df['Totale'].idxmax()]

# 2. Visualizza il prodotto, cliente e totale
prodotto_max_guadagno = max_guadagno['Prodotto']
cliente_max_guadagno = max_guadagno['Cliente']
guadagno_max = max_guadagno['Totale']

print(f"Prodotto: {prodotto_max_guadagno}, Cliente: {cliente_max_guadagno}, Guadagno: {guadagno_max}")


# Esercizio 3: Analisi del Prodotto con il Maggior Guadagno in un Singolo Acquisto

# Obiettivi:



# Trova il prodotto con il maggior guadagno in un singolo acquisto (individuato dal massimo valore nella colonna Totale).

# Mostra il prodotto e il cliente che ha generato il guadagno maggiore.