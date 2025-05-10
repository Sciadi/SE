from pprint import pprint
import json
from constants import UIN, MAPPING_RANK_MODEL
from postgres.postrgres import search_in_postgres
from pylucene.pylucene import pylucene_search
from wo.se_woosh import search
import sys




def search_pg(query, config, rank_model):
    if not query:
        return {"error": "Query vuota"}
    results, sql = search_in_postgres(query, config, rank_model)
    return  results



#results = { uin['query']:{'type':uin['type'], 'pg':{} , 'pyluc':{}, 'wo':{}} for uin in queries_dict }

def do_search(queries_dict):
    results = { uin['query']:{'type':uin['type'], 'pg':{} , 'pyluc':{}, 'wo':{}} for uin in queries_dict }
    print("INIZIO WOOSH ")
    for query in queries_dict:
        system = 'wo'
        uin = query['query']
        config = 'full-text' if query['type'] == 'Full text' else 'title'
        q = query["pylucene"]
        for rank_model in ["BM25", "TF-IDF"]:
            res = search(q, config,weighting=rank_model )
            results[uin][system][rank_model]=res


    # POSTGRES

    print("INIZIO POSTGRES ")
    pg_results = {r:[] for r in MAPPING_RANK_MODEL["PostgreSQL"]}
    for query in queries_dict:
        system = 'pg'
        config = query['type']
        q = query["pylucene"]
        uin = query['query']

        print(f"eseguo {q}")
        for rank_model in MAPPING_RANK_MODEL["PostgreSQL"]:
            res = search_pg(q,config, rank_model)
            results[uin][system][rank_model]=res



    # PYLUCENE
    print("INIZIO PYLUCENE ")

    for query in queries_dict:
        system = 'pyluc'
        uin = query['query']
        config = 'full-text' if query['type'] == 'Full text' else query['type']
        q = query["pylucene"]
        for rank_model in ["BM25", "TF-IDF"]:
            res = pylucene_search(q, similarity_model=rank_model, search_type=config)
            results[uin][system][rank_model]=res

    print("STAMPO I RISULTATI")
    #pprint(results['Identify thrillers on love revenge.'])
    return results


def get_user_data():
    type_input = {
        1: 'Titolo',
        2: 'Full text'
    }
    
    query_type = int(input(f'{type_input}\n'))
    
    query = str(input('Inserisci query:\t'))

    queries_dict = [
        {
            'type':type_input[query_type],
            'query': query,
            'pylucene':query
        }
    ]

    return queries_dict


user_input = int(input('''
                   1: All queries (default)\n
                   2: Manual query\n
'''))


if user_input == 1:
    queries_dict = UIN['queries']
    path = 'final.json' 
elif user_input ==2:
    queries_dict = get_user_data()
    path = 'manual_query_res.json'
    print(queries_dict)
else:
    sys.exit()

results=do_search(queries_dict)

pprint(results)

with open(path,'w') as file:
    file.write(json.dumps(results))
