import os
import csv
from whoosh import index, scoring
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser, QueryParser, OrGroup
from whoosh.query import Term, And


# Directory indice
index_dir = "wo/whoosh_index"

import shutil

if os.path.exists(index_dir):
    shutil.rmtree(index_dir)

os.mkdir(index_dir)

# Schema: cosa cercare e come
schema = Schema(
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    description=TEXT(stored=True, analyzer=StemmingAnalyzer()),
)

# Crea o apre l'indice
if not index.exists_in(index_dir):
    ix = index.create_in(index_dir, schema)
else:
    ix = index.open_dir(index_dir)

# Indicizza CSV
def index_csv(csv_path):
    writer = ix.writer()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            writer.add_document(
                title=row["title"],
                description=row["description"],
            )
    writer.commit()
    print("Indicizzazione completata.")

# Indicizzazione
index_csv("archive/csv/titles.csv")

def search(query_str, search_type="full-text", fields=None, filters=None, weighting=None, top_n=10):
    """
    query_str: testo da cercare
    search_type: 'full-text' o 'keyword'
    fields: lista di campi (se None -> usa 'title' e 'description')
    filters: dizionario opzionale {campo: valore}
    weighting: modello di ranking (es. BM25F(), TF_IDF())
    top_n: quanti risultati mostrare
    """
    if weighting == 'BM25':
        searcher = ix.searcher(weighting = scoring.BM25F())
    else:
        searcher = ix.searcher()

    if True:
        if search_type == "full-text":
            if fields is None:
                fields = ["title", "description"]
            parser = MultifieldParser(fields, schema=ix.schema, group=OrGroup)
        elif search_type == "title":
            fields = ['title']
            parser = QueryParser(fields[0], schema=ix.schema)
        else:
            raise ValueError("search_type deve essere 'full-text' o 'title'")

        query = parser.parse(query_str)

        # Applico eventuali filtri aggiuntivi
        if filters:
            filter_parts = [Term(field, value) for field, value in filters.items()]
            final_query = And([query] + filter_parts)
        else:
            final_query = query

        results = searcher.search(final_query, limit=top_n)

        print(f"\n[Query: '{query_str}' | Tipo: {search_type} | Ranking: {weighting.__class__.__name__}]")
        res=[]
        for hit in results:
            res.append({"rank": hit.score, "title": hit['title'], "description":hit['description'][:100]})
        
        return res
    


#search("space war", model="BM25F")
#search("romantic drama", model="TF-IDF")
