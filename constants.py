FILTRO = [
    "Full text",
    "Titolo",
    "Trama"
]

MAPPING_FILTRO_DB = {
    "Full text":"tsv_mul_movie_title_description_genere_type_name_character_cast",
    "Titolo":"tsv_movie_title",
    "Trama":"tsv_movie_description",
    "CAST-Personaggi":"tsv_mul_credit_name_character",
}

MAPPING_RANK_MODEL={
    "PostgreSQL":["ts_rank","ts_rank_cd"]
    #, "PyLucene", "Whoosh"]
}


UIN={
      "queries": [
        {
          "type": "Titolo",
          "query": "Find movies with the title 'Inception'.",
          "ts_query": "plainto_tsquery('english', 'Inception')",
          "pylucene": "Inception"
        },
        {
          "type": "Titolo",
          "query": "Find movies with the title 'The Blue Lagoon'.",
          "ts_query": "plainto_tsquery('english', 'The Blue Lagoon')",
          "pylucene": "The Blue Lagoon"
        },
        {
          "type": "Titolo",
          "query": "Find movies with the title 'She's Gotta Have It'.",
          "ts_query": "to_tsquery('english', 'She Gotta Have It')",
          "pylucene": "She Gotta Have It"
        },
        {
          "type": "Titolo",
          "query": "Find movies with the title 'Mission: Impossible'.",
          "ts_query": "plainto_tsquery('english', 'Mission: Impossible')",
          "pylucene": "Mission: Impossible"
        },
        {
          "type": "Titolo",
          "query": "Find movies with the title 'Connected'.",
          "ts_query": "to_tsquery('english', 'Connected')",
          "pylucene": "Connected"
        },
        {
          "type": "Full text",
          "query": "Find movies based on real-life public figures or biographies",
          "ts_query": "to_tsquery('english', 'biographical & drama')",
          "pylucene": "biographical drama"
        },
        {
          "type": "Full text",
          "query": "Discover shows on lawyer ",
          "ts_query": "plainto_tsquery('english', 'teen & coming-of-age comedy')",
          "pylucene": "lawyer cases"
        },
        {
          "type": "Full text",
          "query": "Identify thrillers on love revenge.",
          #"ts_query": "to_tsquery('english', 'drug & smuggling & adventure')",
          "pylucene": "love revenge"
        },
        {
          "type": "Full text",
          "query": "Explore stories of young superheroes",
          "ts_query": "to_tsquery('english', 'superhero & high & school')",
          "pylucene": "superhero young"
        },
        {
          "type": "Full text",
          "query": "Based on a true story",
          "ts_query": "phraseto_tsquery('english', 'based on a true story')",
          "pylucene": "based on a true story"
        }
      ]
  }