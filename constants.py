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
          "type": "film",
          "query": "Find movies with the title 'Inception'.",
          "ts_query": "plainto_tsquery('english', 'Inception')"
        },
        {
          "type": "actor",
          "query": "Find movies starring 'Leonardo Di Caprio'.",
          "ts_query": "plainto_tsquery('english', 'Leonardo Di Caprio')"
        },
        {
          "type": "film+actor",
          "query": "Find all movies where 'Robert Downey Jr.' played a superhero.",
          "ts_query": "to_tsquery('english', 'Robert Downey Jr. & superhero')"
        },
        {
          "type": "film",
          "query": "Search for movies containing 'detective' in the description.",
          "ts_query": "plainto_tsquery('english', 'detective')"
        },
        {
          "type": "actor",
          "query": "Which actors have played a 'robot' or an 'alien'?",
          "ts_query": "to_tsquery('english', 'robot | alien')"
        },
        {
          "type": "film+actor",
          "query": "Which movies featuring 'Angelina Jolie' contain the word 'espionage' in the description?",
          "ts_query": "to_tsquery('english', 'Angelina Jolie & espionage')"
        },
        {
          "type": "film",
          "query": "Show all movies classified as 'thriller'.",
          "ts_query": "plainto_tsquery('english', 'thriller')"
        },
        {
          "type": "film+actor+character+genres",
          "query": "Find all 'action' movies where 'Christian Bale' played 'Batman'.",
          "ts_query": "to_tsquery('english', 'Christian Bale & Batman & action')"
        },
        {
          "type": "film+actor",
          "query": "Search for 'thriller' movies where 'Morgan Freeman' plays a detective.",
          "ts_query": ""
        },
        {
          "type": "film",
          "query": "Show movies with the exact phrase 'based on a true story' in the description.",
          "ts_query": "phraseto_tsquery('english', 'based on a true story')"
        }
      ]
  }
