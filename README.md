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
ts_rank	-> Punteggio basato solo sulla frequenza dei termini: Un ranking veloce e semplice
ts_rank_cd	-> Punteggio basato su frequenza e densità per  un ranking più accurato
Il peso di un match ordinato con phraseto_tsquery è doppio rispetto a quello generico con phraseto_tsquery.
(Falso positivo con Johnny Deep, la ricerca full text mi restituiva un film che aveva Deep nel titolo e Johnny nel cast: ho quindi dato peso doppio al match ordinato)
