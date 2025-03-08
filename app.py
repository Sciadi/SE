from flask import Flask, request, jsonify
import json

from postgres.postrgres import search_in_postgres
#from your_pylucene_module import pylucene_search  # Modifica con il tuo modulo
#from your_whoosh_module import whoosh_search  # Modifica con il tuo modulo

app = Flask(__name__)



@app.route("/search_pg", methods=["PUT"])
def search_pg():
    query = None
    data = json.loads(request.json)
    query = data["query"]
    config = data["config"]
    rank_model = data["rank_model"]
    if not query:
        return jsonify({"error": "Query vuota"}), 400
    results = search_in_postgres(query, config, rank_model)
    return jsonify({"results": results})

"""@app.route("/search_lucene", methods=["GET"])
def search_lucene():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Manca il parametro 'q'"}), 400
    results = pylucene_search(query)
    return jsonify({"results": results})

@app.route("/search_whoosh", methods=["GET"])
def search_whoosh():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Manca il parametro 'q'"}), 400
    results = whoosh_search(query)
    return jsonify({"results": results})"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
