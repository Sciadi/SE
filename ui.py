import streamlit as st
import requests

# Configura il titolo della UI
st.title("Motore di Ricerca - Confronto Search Engine")

# Barra di ricerca per l'input dell'utente
query = st.text_input("🔍 Inserisci la tua ricerca e premi Invio", "")

# Selettore per il search engine da interrogare
search_engine = st.selectbox(
    "🔀 Seleziona il motore di ricerca",
    ["PostgreSQL", "PyLucene", "Whoosh"]
)

# Mappa il nome del search engine all'endpoint corrispondente
ENDPOINTS = {
    "PostgreSQL": "http://localhost:5000/search_pg",
    "PyLucene": "http://localhost:5000/search_lucene",
    "Whoosh": "http://localhost:5000/search_whoosh"
}

if query:
    endpoint = ENDPOINTS.get(search_engine)
    response = requests.get(f"{endpoint}?q={query}")

    if response.status_code == 200:
        results = response.json().get("results", [])

        if results:
            st.write(f"### 📌 Risultati trovati con {search_engine} ({len(results)})")
            
            for i, result in enumerate(results, 1):
                st.markdown(f"**{i}. [{result['title']}]({result['url']})**")
                st.write(result["snippet"])
                st.markdown("---")
        else:
            st.write("❌ Nessun risultato trovato.")
    else:
        st.write("⚠️ Errore nel recupero dei dati.")
