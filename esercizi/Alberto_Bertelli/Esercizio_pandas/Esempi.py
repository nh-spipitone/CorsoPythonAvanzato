import pandas as pd

# 1. Creazione del DataFrame
data = {
'ID_Studente': [1, 2, 3, 4, 5, 6, 7, 8],
'Nome': ['Alice', 'Marco', 'Giulia', 'Luca', 'Sara', 'Pietro', 'Elena', 'Francesco'],
'Matematica': [28, 22, 30, 24, 27, 19, 26, 23],
'Fisica': [25, 28, 30, 20, 22, 24, 27, 21],
'Informatica': [30, 27, 29, 25, 26, 23, 28, 24]
}

df = pd.DataFrame(data)

# 2. Aggiungere colonna Media
df['Media'] = df[['Matematica', 'Fisica', 'Informatica']].mean(axis=1)

# 3. Filtraggio studenti con media >= 27
studenti_buoni = df[df['Media'] >= 27]

# 4. Ordinamento in ordine decrescente di media
studenti_buoni = studenti_buoni.sort_values(by='Media', ascending=False)

print(studenti_buoni)

# 5. Raggruppamento (opzionale)
gruppo = df.groupby(df['Matematica'] >= 27)[['Fisica', 'Informatica']].mean()
print("\nMedia Fisica e Informatica per gruppo Matematica >= 27:")
print(gruppo)