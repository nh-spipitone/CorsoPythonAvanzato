# Libreria OS

### Come si importa?

```python
   import os
```

### Funzioni principali

```python
   os.getcwd() #ritorna la cartella corrente
   os.listdir(path) #ritorna la lista di directory/folder in una cartella di cui noi diamo il path
   os.makedirs(path, exist_ok=True) #crea cartelle annidate nel path
   os.remove(path) # elimina cartella o file
   os.rename(src,dst) #rinomina danto prima il path della cartella o file e poi come vorremmo rinominarlo
   os.environ.get("NOME_VAR") #leggi variabili d' ambiente
   os.path.join(a,b,...) # unire parti di path
   os.path.exists(path)  #verifica se un path essiste e ritorna vero o falso
```

# open

### come funziona open?

```python

  with open("nomefile.estensione","modalità di scrittura",encoding="utf-8") as f:
    contenuto= f.read()
    f.write("ciao")


 #esempi specifici

 with open("file.txt","r",encoding="utf-8") as file:
    contenuto=f.read()
    contenuto_lines= f.readlines()
    contenuto= f.readline()
    for riga in f:
        print(riga)


 listalinee=["ciaoo come stai\n","io bene"]
 with open("file.txt","w",encoding="utf-8") as file:
    f.write("ciao\n")
    f.writelines(listalinee)

#append a differenza di write non sovrascrive ma appende il suo contenuto aggiungendolo

 with open("file.txt","a",encoding="utf-8") as file:
    f.write("riga...\n")

```

# Modulo Json

### come si importa il modulo json?

```python
 import json
 #struttura json

 esempio= {"nome": "Simone","skills":["python","django"],"active":True}

 esempio_json= json.dumps(data,indent=2)


```
