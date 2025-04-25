import lucene
lucene.initVM()
import csv
from org.apache.lucene.document import Document, TextField, StringField, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search.similarities import BM25Similarity, ClassicSimilarity
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher, BooleanClause
from org.apache.lucene.search.similarities import ClassicSimilarity, BM25Similarity
#from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from java.nio.file import Paths
from java.lang import String, CharSequence


# Define index directory
index_dir = "./index_directory"
directory = FSDirectory.open(Paths.get(index_dir))

# Analyzer for processing text
analyzer = StandardAnalyzer()

# Index Writer configuration
config = IndexWriterConfig(analyzer)
index_writer = IndexWriter(directory, config)

# Indexing CSV file
def index_csv(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc = Document()
            doc.add(TextField("title", row["title"], Field.Store.YES))
            doc.add(TextField("type", row["type"], Field.Store.YES))
            doc.add(TextField("description", row["description"], Field.Store.YES))
            doc.add(StringField("release_year", row["release_year"], Field.Store.YES))
            doc.add(TextField("genres", row["genres"], Field.Store.YES))
            index_writer.addDocument(doc)

# Index the uploaded file
csv_path = "../archive/csv/titles.csv"
index_csv(csv_path)
index_writer.commit()
index_writer.close()
print("Indexing completed.")

# Function to search using different ranking models
def search(query_str, similarity_model="BM25", search_type="keyword", top_n=10):
    index_reader = DirectoryReader.open(directory)
    index_searcher = IndexSearcher(index_reader)
    
    # Apply ranking model
    if similarity_model == "BM25":
        index_searcher.setSimilarity(BM25Similarity())
    elif similarity_model == "TF-IDF":
        index_searcher.setSimilarity(ClassicSimilarity())
    
    fields = ["title", "type", "description", "genres"]
    if search_type == "keyword":        
        SHOULD = [BooleanClause.Occur.SHOULD]*len(fields)
        query = MultiFieldQueryParser.parse(query_str,fields,SHOULD,analyzer)
    else:  # Full-text query
        query_parser = QueryParser("description", analyzer)
        query = query_parser.parse(query_str)
    
     
    
    top_docs = index_searcher.search(query, top_n)
    
    # Print search results
    print(f"\nResults for '{query_str}' using {similarity_model} ({search_type} search):")
    for score_doc in top_docs.scoreDocs:
        doc = index_searcher.doc(score_doc.doc)
        print(f"Score: {score_doc.score:.4f}, Title: {doc.get('title')}, Type: {doc.get('type')}, Year: {doc.get('release_year')}, Genres: {doc.get('genres')}, Description: {doc.get('description')}")
    
    index_reader.close()

# Example queries
search("example title", similarity_model="BM25", search_type="keyword")
search("example title", similarity_model="BM25", search_type="full-text")
search("example title", similarity_model="TF-IDF", search_type="keyword")
search("example title", similarity_model="TF-IDF", search_type="full-text")
