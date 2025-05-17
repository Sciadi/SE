# SE
 SearchEngine (Pylucene Whoosh Postgres)

## Descrizione generale
Tutto è configurato tramite file, le uin e le query sono nel file -> *constants.py*.
Lo script **app.py** lancia l'esecuzione delle ricerche sui vari SE; ad ogni lancio dello script:
- Postgres lancia query sul db mentre gli altri 2 leggono i dati dal percorso *archive/csv/tiles.csv*. 
  __Le tabelle del db sono state create con i comandi in db/genesi.sql__

- Woosh e Pylucene puliscono l'ambiente, indicizzano il dataset ed eseguono le query; 

Una volta runnati i S.E. salviamo l'esito delle query in final.json. 

**è sufficiente formattare il json per rendere leggibili i risultati delle query**

Successivamente ho aggiunto manualmente e interattivamente le valutazioni nel file **valutazioni_rilevanza.json** grazie allo script *assegna_rilevanza.py* aggiungendo la chiave *"rilevante"* e un valore compreso tra 0 e 1 in base alla rilevanza del risultato rispetto alla UIN. 

Infine in base a questi dati ho elaborato i benchmarks. 
Lo script **calcola_benchmarks.py** legge i dati da **benchmark.json** e calcola MAP Precisione e NCDG, assegnando un valore medio ad ogni metrica per tutte le UIN. 

Nel caso di query manuale non ho inserito la possibilità di valutare la rilevanza dei risultati.

# Installazione
### 1 - Installare dependencies  
```pip install -r requirements.txt``` (progetto con macchina linux/ubuntu 24 pylucene installato) 

### 2.1 - File constants.py 
In base a questa costante possiamo eseguire query:
- la chiave **query** riporta la uin in linguaggio naturale 
- la chiave **ts_query** definisce la query desiderata per postgresql
- la chiave **pylucene** definisce la query per pylucene e whoosh 

Configurazione file query:

UIN={
      "queries": [
        {
          "type": "Titolo",
          "query": "Find movies with the title 'Inception'.",
          "ts_query": "plainto_tsquery('english', 'Inception')",
          "pylucene": "Inception"
        },
       .
       .
       .
       ]
       }



### 2.2 - Avviare SE (posizionarsi su cartella SE)
```python app.py```

Interagire con la linea di comando. 

#### Il campo Titolo 

### 3 - Risultati query
Tutti i risultati delle query sono ispezionabili in 'final.json' che riporta il rank assegnato dai vari ranking model.
Nel caso di query manuale i risultati sono in manual_query_res.json

#### Configurazione POSTGRES
Il DB è hostato su aiven.com, se inutilizzato va in stand-by quindi potrebbe non essere attivo. 

- ts_rank	-> Punteggio basato solo sulla frequenza dei termini: Ranking veloce e semplice
- ts_rank_cd	-> Punteggio basato su frequenza e densità per un ranking più accurato Analogo a TF-IDF

Il peso di un match ordinato con phraseto_tsquery è *doppio* rispetto a quello generico con to_tsquery perche' il primo matcha il virgolettato e per evitare i falsi positivi:
-> Falso positivo con Johnny Deep, la ricerca full text mi restituiva un film che aveva Deep nel titolo e Johnny nel cast: ho quindi dato peso doppio al match che considera l'ordinamento delle parole

#### Configurazione pylucene e Woosh
Usiamo 
    Bm25:  Tiene conto della lunghezza del documento,
           della frequenza dei termini,
           del numero totale di documenti. 
           Più preciso e moderno per casi reali di ricerca testuale

    TF-IDF: Calcola l'importanza di una parola in base alla frequenza nel documento (TF),
            e di quanti documenti contengono quella parola (IDF).


