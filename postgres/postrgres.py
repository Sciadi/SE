import psycopg2

# Configurazione del database PostgreSQL
DB_CONFIG = {
    "dbname": "movie_search_engine",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}



# PostgreSQL Full-Text Search
def search_in_postgres(query):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    sql = f"""
    SELECT id, title, description
    FROM movies 
    WHERE id = {query}
    LIMIT 10;
    """
    #ORDER BY ts_rank(tsv, to_tsquery('italian', %s)) DESC
    cur.execute(sql, (query.replace(" ", " & "), query.replace(" ", " &")))
    results = [{"title": row[1], "snippet": row[2][:200], "url": f"http://example.com/{row[0]}"} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results
