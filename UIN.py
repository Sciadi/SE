UIN={
      "queries": [
        {
          "type": "film",
          "query": "Find movies with the title 'Inception'.",
          "ts_query": "plainto_tsquery('english', 'Inception')",
          "pylucene": "Inception"
        },
        {
          "type": "cast",
          "query": "Find movies starring 'Leonardo Di Caprio'.",
          "ts_query": "plainto_tsquery('english', 'Leonardo Di Caprio')",
          "pylucene": "Leonardo Di Caprio"
        },
        {
          "type": "film+cast",
          "query": "Find all movies where 'Robert Downey Jr.' played a superhero.",
          "ts_query": "to_tsquery('english', 'Robert Downey Jr. superhero')",
          "pylucene": "Robert Downey Jr superhero"
        },
        {
          "type": "film",
          "query": "Search for movies containing 'detective' in the description.",
          "ts_query": "plainto_tsquery('english', 'detective')",
          "pylucene": "detective"
        },
        {
          "type": "cast",
          "query": "Which casts have a 'robot' or an 'alien'?",
          "ts_query": "to_tsquery('english', 'robot | alien')",
          
        },
        {
          "type": "full text",
          "query": "Which movies featuring 'Leonardo Di Caprio' contain the word 'espionage' in the description?",
          "ts_query": "to_tsquery('english', 'Leonardo Di Caprio & espionage')",
          "pylucene": "Leonardo Di Caprio espionage"
        },
        {
          "type": "genres",
          "query": "Show all movies classified as 'thriller'.",
          "ts_query": "plainto_tsquery('english', 'thriller')",
          "pylucene": "thriller"
        },
        {
          "type": "full text",
          "query": "Find all 'action' movies where 'Christian Bale' played 'Batman'.",
          "ts_query": "to_tsquery('english', 'Christian Bale & Batman & action')",
          "pylucene": "Batman Christian Bale"
        },
        {
          "type": "full text",
          "query": "Search for 'thriller' movies where 'Morgan Freeman' plays a detective.",
          "ts_query": "to_tsquery('english', 'Morgan Freeman & detective')",
          "pylucene": "thriller morgan freeman detective"
        },
        {
          "type": "full text",
          "query": "Show movies with the exact phrase 'based on a true story' in the description.",
          "ts_query": "phraseto_tsquery('english', 'based on a true story')",
          "pylucene": "based on a true story"
        }
      ]
  }