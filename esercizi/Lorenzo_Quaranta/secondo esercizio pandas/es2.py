'''

Esercizio: Analisi delle Vendite di un Negozio (Versione Semplificata)



Immagina di avere i dati delle vendite di un negozio, con le seguenti colonne:

ID_Transazione: Un identificativo univoco per ogni transazione

Cliente: Il nome del cliente che ha effettuato l'acquisto

Prodotto: Il prodotto acquistato

Quantità: Il numero di unità acquistate

Prezzo: Il prezzo per unità del prodotto acquistato

Obiettivo dell'esercizio:

Creazione del DataFrame:

Crea un DataFrame Pandas con 10 righe di dati. I dati devono contenere:

ID_Transazione: Numeri da 1 a 10.

Cliente: "Cliente1", "Cliente2", ..., "Cliente10".

Prodotto: "Prodotto1", "Prodotto2", "Prodotto3".

Quantità: Un numero casuale tra 1 e 5.

Prezzo: Un numero casuale tra 5 e 30.

Esplorazione del DataFrame:

Visualizza le prime 5 righe del DataFrame con df.head().

Verifica se ci sono valori nulli nel DataFrame con df.isnull().sum().


Creazione di una Nuova Colonna:

Crea una nuova colonna chiamata Totale che calcoli il totale per ogni transazione (ovvero Quantità * Prezzo).

Filtraggio dei Dati:

Filtra il DataFrame per selezionare solo le transazioni con una Quantità maggiore di 3.

Raggruppamento per Prodotto:

Raggruppa i dati per Prodotto e calcola la somma totale delle vendite (colonna Totale) per ogni prodotto.
Ordinamento dei Dati:
Ordina il DataFrame in ordine crescente in base alla colonna Totale

'''
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

# Visualizzazione dei risultati finali
print("\nVendite per Prodotto:")
print(vendite_per_prodotto)
print("\nDataFrame Ordinato:")
print(df_ordinato)

'''Esercizio 2: Analisi dei Prodotti Più Venduti

In questo esercizio, i ragazzi dovranno analizzare i dati delle vendite 
per determinare quali sono i prodotti più venduti in base alla quantità venduta.

Obiettivi:

Raggruppa i dati per Prodotto e calcola la somma delle quantità vendute.

Ordina i risultati in ordine decrescente per quantità.

Mostra solo i primi 3 prodotti più venduti.

'''
print("\n3 prodotti più venduti:")
top3_quantita=(df.groupby("Prodotto")["Quantità"]
         .sum()
         .head(3)
         .rename("Vendite totali")
         .sort_values(ascending=False)
         .reset_index())
print(top3_quantita)

'''Esercizio 3: Analisi del Cliente con il Maggior Totale Acquistato
Obiettivi:
Raggruppa i dati per Cliente e calcola la somma totale delle vendite per ciascun cliente.

Ordina i risultati in ordine decrescente per somma totale.

Mostra il cliente che ha speso di più.'''
print("\nCliente più spendaccione:")
top_clienti=(df.groupby("Cliente")["Totale"]
         .sum()
         .sort_values(ascending=False)
         .head(1)
         .rename("Acquisti")
         .reset_index())
print(top_clienti)

'''
Esercizio 4: Analisi del Prodotto con il Maggior Guadagno in un Singolo Acquisto

Obiettivi:

Calcola il totale per ogni transazione (è già presente nel DataFrame come Totale).

Trova il prodotto con il maggior guadagno in un singolo acquisto (individuato dal massimo valore nella colonna Totale).

Mostra il prodotto e il cliente che ha generato il guadagno maggiore.
'''
miglior_acquisto=df[['Prodotto','Cliente','Totale']].sort_values(by=['Totale'],ascending=False).head(1)
print("\nMiglior acquisto:")
print(miglior_acquisto)