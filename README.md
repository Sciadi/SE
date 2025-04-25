# SE
 SearchEngine


## Avviare BE 
```python app.py```

## Avviare UI

```python ui.py```

(Unire i comandi)

### Regole POSTGRES
, per or 
AND '&' non va specificato, lo spazio è sufficiente
Per specificare il ruolo di un attore: Nome Cognome#Personaggio
ts_rank	-> Punteggio basato solo sulla frequenza dei termini: Ranking veloce e semplice
ts_rank_cd	-> Punteggio basato su frequenza e densità per un ranking più accurato Analogo a TF-IDF
Il peso di un match ordinato con phraseto_tsquery è doppio rispetto a quello generico con phraseto_tsquery perche' il primo matcha il virgolettato e per evitare i falsi positivi:

- Falso positivo con Johnny Deep, la ricerca full text mi restituiva un film che aveva Deep nel titolo e Johnny nel cast: ho quindi dato peso doppio al match ordinato

### Regole pylucene
Usiamo 
    Bm25:  Tiene conto della lunghezza del documento,
           della frequenza dei termini,
           del numero totale di documenti. 
           Più preciso e moderno per casi reali di ricerca testuale

    TF-IDF: Calcola l'importanza di una parola in base alla frequenza nel documento (TF),
            e di quanti documenti contengono quella parola (IDF).

### Regole Woosh 
Usiamo 
    TF-IDF: Basato su Term Frequency e Inverse Document Frequency
    Frequency: Ordina solo in base a quante volte un termine appare nel documento (TF puro)