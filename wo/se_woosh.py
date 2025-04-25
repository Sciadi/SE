import os
import csv
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser
from whoosh.qparser import MultifieldParser
from whoosh import scoring


# Directory indice
index_dir = "whoosh_index"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

# Schema: cosa vuoi cercare e come
schema = Schema(
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    type=TEXT(stored=True),
    description=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    release_year=ID(stored=True),
    genres=KEYWORD(stored=True, commas=True, lowercase=True)
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
                type=row["type"],
                description=row["description"],
                release_year=row["release_year"],
                genres=row["genres"]
            )
    writer.commit()
    print("Indicizzazione completata.")

# Esegui indicizzazione
index_csv("titles_cleaned.csv")



def search(query_str, model="BM25F", top_n=10):
    if model == "BM25F":
        scoring_fn = scoring.BM25F()
    elif model == "TF-IDF":
        scoring_fn = scoring.TF_IDF()
    else:
        raise ValueError("Modello di ranking non valido. Usa 'BM25F' o 'TF-IDF'.")

    with ix.searcher(weighting=scoring_fn) as searcher:
        parser = MultifieldParser(["title", "description", "genres"], schema=ix.schema)
        query = parser.parse(query_str)

        results = searcher.search(query, limit=top_n)
        print(f"\nRisultati per '{query_str}' con modello {model}:")
        for hit in results:
            print(f"Score: {hit.score:.4f}, Title: {hit['title']}, Type: {hit['type']}, Year: {hit['release_year']}, Genres: {hit['genres']}")

# Esempi
search("space war", model="BM25F")
search("romantic drama", model="TF-IDF")
