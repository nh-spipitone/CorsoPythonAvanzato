'''Esercizio 5: Creazione e Analisi di un DataFrame di Studenti

In questo esercizio, gli studenti dovranno creare un DataFrame che rappresenta i voti di alcuni studenti in diverse materie e poi fare semplici operazioni di analisi.

Dati da inserire nel DataFrame:

Gli studenti dovranno creare un DataFrame con le seguenti colonne:

ID_Studente: Numeri da 1 a 8

Nome: Nomi degli studenti (puoi usare nomi fittizi come "Alice", "Marco", "Giulia", ecc.)

Matematica: Voti in matematica (numeri interi tra 18 e 30)

Fisica: Voti in fisica (numeri interi tra 18 e 30)

Informatica: Voti in informatica (numeri interi tra 18 e 30)

Operazioni da fare:

Creazione del DataFrame usando i dati sopra.

Aggiungere una colonna "Media" che calcoli la media dei voti per ciascuno studente.

Filtraggio dei dati:

Seleziona gli studenti con media maggiore o uguale a 27.

Ordinamento dei dati:

Ordina gli studenti in ordine decrescente di media.

Raggruppamento (opzionale):

Se vuoi introdurre il concetto di raggruppamento, raggruppa per "Matematica >= 27" e calcola la media in Fisica e Informatica dei due gruppi.
'''
import pandas,random
random.seed()
data={
    "ID_Studente": [1,2,3,4,5,6,7,8],
    "Nome":["Andreo","Marca","Scianel","Luco","Adolfa","Nadio","X Æ A-12","Peppone"],
    "Matematica": [random.randrange(18,30) for n in range(8)],
    "Fisica": [random.randrange(18,30) for n in range(8)],
    "Informatica": [random.randrange(18,30) for n in range(8)]
}

df_studenti=pandas.DataFrame(data)

print(df_studenti)

df_studenti["Media"]=(df_studenti["Matematica"]+df_studenti["Fisica"]+df_studenti["Informatica"])/3


print("\n modificato:")
print(df_studenti)