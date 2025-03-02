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
    query = re.sub(r'\s*,\s*', ',', input_text)
    print(input_text)
    
    # Sostituisce gli spazi con " & " 
    query = re.sub(r'\s+', ' & ', query)
    print(query)

    # Sostituisce le virgole con " | " 
    query = re.sub(r'\s*,\s*', ' | ', query)
    print(query)
    
    return query


# PostgreSQL Full-Text Search
def search_in_postgres(query, config):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    vector = MAPPING_FILTRO_DB[config]
    
    #words = query.split(' ')
    #words = ",".join(f'"{w}"' for w in words)
    words = crea_ts_query(query)
    print(words)

    if config == "CAST-Personaggi":
        join_v = join() 
    else:
        join_v = ''
        field =''
    

    sql = f"""
    SELECT m.id, m.title, m.description, m."cast"
    FROM movies m {join_v}
    WHERE to_tsquery('{words}') @@ {vector}
    ;
    """
    #ORDER BY ts_rank(tsv, to_tsquery('italian', %s)) DESC

    print(f"Eseguo query:\n{sql}\n")

    
    cur.execute(sql)
    #print(cur.fetchall())
    results = [{"cast":row[3], "description": row[2][:200],"title": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results
