import json
from constants import UIN, MAPPING_RANK_MODEL
from postgres.postrgres import search_in_postgres
from pylucene.pylucene import pylucene_search

#from your_pylucene_module import pylucene_search  # Modifica con il tuo modulo
#from your_whoosh_module import whoosh_search  # Modifica con il tuo modulo






def search_pg(query, config, rank_model):
    if not query:
        return {"error": "Query vuota"}
    results, sql = search_in_postgres(query, config, rank_model)
    return  results



"""@app.route("/search_whoosh", methods=["GET"])
def search_whoosh():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Manca il parametro 'q'"}), 400
    results = whoosh_search(query)
    return jsonify({"results": results})"""

queries_dict = UIN['queries']
results = { uin['query']:{'pg':{} , 'pyluc':{}, 'wo':{}} for uin in queries_dict }


# POSTGRES

from pprint import pprint
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
pprint(results['Identify thrillers on love revenge.'])


# WOOSH




# TODO: depositare results in un json per confrontare i risultati per uin 
#
# DESIDERATA
# Per ogni uin -> system-> per ogni system il rank model. Così si possono confrontare per uin
"""
{
    uin: ["system":{
            "rank_model":---
                results: [{
                    title:
                    description:
                    rank:
                },
                .
                .
                .
                ]
            },
            "rank_model":---
                    results: [{
                    title:
                    description:
                    rank:
                },
                .
                .
                .
                ]
            },
        .
        .
        .
        ]
}
"""