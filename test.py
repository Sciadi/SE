import lucene
lucene.initVM()
import csv
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import IndexSearcher, BooleanClause

analyzer = StandardAnalyzer()

query_str = 'Inception'

fields = ['title']
SHOULD = [BooleanClause.Occur.SHOULD]

query = MultiFieldQueryParser.parse(query_str,[fields[0]],SHOULD,analyzer)

print(query)