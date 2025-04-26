import psycopg2
import re
from constants import MAPPING_FILTRO_DB 

# Configurazione del database PostgreSQL
DB_CONFIG = {
    "dbname": "defaultdb",
    "user": "avnadmin",
    "password": "AVNS_OU3OvwZAIP9zkjvsA5G",
    "host": "pg-sengine-search-engine1234.l.aivencloud.com",
    "port": "25760"
}

def join():
    join_sql = """
    JOIN movies_credits mc 
    ON mc.movie_id = m.id
    JOIN credits c
    ON c.id = mc.credit_id"""
    return join_sql

def crea_ts_query(input_text):
    # Rimuove spazi inutili e normalizza la stringa
    input_text = input_text.strip()
    input_text = input_text.replace('&','')
    query = re.sub(r'\s*,\s*', ',', input_text)
    
    # Sostituisce gli spazi con " & " 
    query = re.sub(r'\s+', ' & ', query)
    # Sostituisce le virgole con " | " 
    query = re.sub(r'\s*,\s*', ' | ', query)
    
    return query


# PostgreSQL Full-Text Search
def search_in_postgres(query, config, rank_model):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print(config)

    vector = MAPPING_FILTRO_DB[config]
    
    words = crea_ts_query(query)
    print(words)

#    if config == "CAST-Personaggi":
#        join_v = join() 
#   else:
    join_v = ''
    field =''
    
    # Quando uso phraseto_tsquery assegno peso doppio al match perche' il primo matcha il virgolettato
    rank = dict(
        ts_rank = f"2*pg_catalog.ts_rank({vector}, phraseto_tsquery('{words}'))+pg_catalog.ts_rank({vector}, to_tsquery('{words}'))",
        ts_rank_cd = f"2*pg_catalog.ts_rank_cd({vector}, phraseto_tsquery('{words}'))+pg_catalog.ts_rank_cd({vector}, to_tsquery('{words}'))"
        )
    

    sql = f"""
    SELECT m.id, m.title, m.description, m."cast", 
    {rank[rank_model]} as rank
    FROM movies m {join_v}
    WHERE 1=1
    AND to_tsquery('{words}') @@ {vector}
    order by rank DESC
    ;
    """
    #ORDER BY ts_rank(tsv, to_tsquery('italian', %s)) DESC

    print(f"Eseguo query:\n{sql}\n")

    
    cur.execute(sql)
    results = [{"description": row[2][:100],"title": row[1], "rank":row[4]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results, sql
