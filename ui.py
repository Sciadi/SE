import streamlit as st
import requests
import json
from constants import FILTRO, MAPPING_RANK_MODEL

def get_config(query):
    res = {"config": filtro, "rank_model": ranking_model}
    res["query"]= query
    return json.dumps(res)
    

# Configura il titolo della UI
st.title("Motore di Ricerca - Confronto Search Engine ")

# Barra di ricerca per l'input dell'utente
query = st.text_input("🔍 Inserisci la ricerca e premi Invio", "")


# Selettore per il SE
columns = st.columns([2,2,2])
search_engine = columns[0].selectbox(
    "🔀 Seleziona il motore di ricerca",
    ["PostgreSQL", "PyLucene", "Whoosh"]
)

# Selettore per il Tipo di ricerca
filtro = columns[1].selectbox(
    "Seleziona il Tipo di Ricerca",
    [elem for elem in FILTRO]
) 

ranking_model = columns[2].selectbox(
    "💯 Rank model",
    MAPPING_RANK_MODEL[search_engine]
)


# Mappa il nome del search engine all'endpoint corrispondente
ENDPOINTS = {
    "PostgreSQL": "http://localhost:5001/search_pg",
    "PyLucene": "http://localhost:5001/search_lucene",
    "Whoosh": "http://localhost:5001/search_whoosh"
}

if query:
    endpoint = ENDPOINTS.get(search_engine)
    data = get_config(query)

    response = requests.put(url=endpoint,json=data)
    
    if response.status_code == 200:
        results = response.json().get("results", [])

        if results:
            st.write(f"### 📌 {len(results)} Risultati trovati con {search_engine}")
            
            for i, result in enumerate(results, 1):
                st.markdown(f"Titolo : {result["title"]}, rank : {result["rank"]}")
                result.pop("title")
                result.pop("rank")
                st.write(result)
                #st.write(result["snippet"])
                st.markdown("---")
        else:
            st.write("❌ Nessun risultato trovato.")
    else:
        print(response.text)
        st.write("⚠️ Errore nel recupero dei dati.")
