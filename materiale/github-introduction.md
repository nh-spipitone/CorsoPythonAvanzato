# Comandi Base

### config autenticazione

```bash
git config --global user.name "nome-github"
git config --global user.email "email@dominio.com"
```

### Inizializzare la repo

```bash
git init
```

### Capire lo stato dei file

```bash
git status
```

Ci dice cosa abbiamo modificato e cosa in staging(pronto per la commit)

### Aggiungere file allo staging

```bash
git add <file> # aggiunge il file specificato
git add . #aggiunge tutto ciò che è cambiato
```

se sbagliamo ce

```bash
git restore --staged <file> #toglie il file dallo stage
```

### Fare una commit

```bash
git commit -m "feat: cosa hai fatto e perché"
```

### Caricare sulla repo

```bash
git push
```

### aggiornare e mergiare nel branch corrente

```bash
git pull
```

### Creare una branch

```bash
git switch -c "nome-branch"
git add .
git commit -m "prima commit"
git push -u origin nome-branch
```
