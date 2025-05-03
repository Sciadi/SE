import json
from collections import defaultdict
from sklearn.metrics import ndcg_score, average_precision_score
import numpy as np
import matplotlib.pyplot as plt


# Carica il file JSON dal percorso caricato
file_path = "benchmark.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalizza e raccoglie i risultati
results = defaultdict(lambda: defaultdict(list))  


for query, engines in data.items():
    for engine, models in engines.items():
        if engine == "type":
            continue
        for model, docs in models.items():
            key = f"{engine}.{model}"
            for i, doc in enumerate(docs):
                try:
                    rel = float(doc["rilevante"])
                except:
                    rel = 0.0
                results[key][query].append(rel)

#print(results['pyluc.BM25'])
#print(len(results['pyluc.BM25']))

# Funzioni di metrica
def precision_at_k(relevances, k=10):
    top_k = relevances[:k]
    return np.mean([1 if r > 0 else 0 for r in top_k]) if top_k else 0.0

def recall(relevances):
    total_relevant = sum(1 for r in relevances if r > 0)
    retrieved_relevant = sum(1 for r in relevances[:len(relevances)] if r > 0)
    return retrieved_relevant / total_relevant if total_relevant else 0.0

# Calcolo metriche
def compute_metrics(results):
    metrics = {}
    detail = {}
    for key, queries in results.items():
        ndcgs, maps, precisions, recalls = [], [], [], []

        for uin, rels in queries.items():
            rels = [float(r) for r in rels]
            binary_rels = [1 if r > 0 else 0 for r in rels]
            scores = list(reversed(range(len(rels))))  # ranking decrescente

            # Se nessun documento e' rilevante metto 0
            if sum(binary_rels) == 0:
                if uin not in detail:
                    detail[uin] = {}    
                detail[uin][key] = {
                    "Precision@10": 0,
                    #"Recall": np.mean(recalls),
                    "MAP": 0,
                    "NDCG@10": 0,
                }
                continue

            precisions.append(precision_at_k(binary_rels, k=10))
            #recalls.append(recall(binary_rels))
            maps.append(average_precision_score(binary_rels, scores))
            ndcgs.append(ndcg_score([binary_rels], [scores], k=10) if len(binary_rels) >1 else binary_rels[0])
            if uin not in detail:
                detail[uin] = {}    
            detail[uin][key] = {
                "Precision@10": np.mean(precisions),
                #"Recall": np.mean(recalls),
                "MAP": np.mean(maps),
                "NDCG@10": np.mean(ndcgs),
            }


        try:
            metrics[key] = {
                "Precision@10": np.mean(precisions),
                #"Recall": np.mean(recalls),
                "MAP": np.mean(maps),
                "NDCG@10": np.mean(ndcgs),
            }
        except:
            print(ndcgs)
            raise
    return metrics, detail

# Calcola e mostra le metriche
final_metrics, detail = compute_metrics(results)
final_metrics_sorted = dict(sorted(final_metrics.items()))
print(final_metrics_sorted)
print(detail)


data = final_metrics_sorted

# Estrai i nomi dei modelli
models = list(data.keys())

# Estrai i valori per Precision@10, MAP e NDCG@10
precision_values = [data[model]['Precision@10'] for model in models]
map_values = [data[model]['MAP'] for model in models]
ndcg_values = [data[model]['NDCG@10'] for model in models]

# Set up la figura
x = np.arange(len(models))  # Posizioni per le barre
width = 0.25  # Larghezza delle barre

# Crea il grafico a barre
fig, ax = plt.subplots(figsize=(10, 6))

rects1 = ax.bar(x - width, precision_values, width, label='Precision@10')
rects2 = ax.bar(x, map_values, width, label='MAP')
rects3 = ax.bar(x + width, ndcg_values, width, label='NDCG@10')

# Aggiungi il titolo e le etichette
ax.set_xlabel('Modelli')
ax.set_ylabel('Valori delle metriche')
ax.set_title('Confronto delle metriche tra modelli')
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha='right')
ax.legend()

# Funzione per aggiungere le etichette sopra le barre
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # Sposta le etichette sopra le barre
                    textcoords="offset points",
                    ha='center', va='bottom')

# Aggiungi le etichette alle barre
add_labels(rects1)
add_labels(rects2)
add_labels(rects3)

# Mostra il grafico
plt.tight_layout()
plt.show()


data = detail
from pprint import pprint
pprint(data)

metrics = ['Precision@10', 'MAP', 'NDCG@10']
models = list(next(iter(data.values())).keys())
num_metrics = len(metrics)
num_uins = len(data)
width = 0.2

# Calcola il layout migliore per i sottografici
cols = 2
rows = int(np.ceil(num_uins / cols))

fig, axs = plt.subplots(rows, cols, figsize=(cols * 6, rows * 5))
axs = axs.flatten()  # semplifica l'indicizzazione anche se c'è solo 1 riga

for idx, (uin, model_scores) in enumerate(data.items()):
    ax = axs[idx]
    x = np.arange(num_metrics)
    print(uin)
    for i, model in enumerate(models):
        
        print(f'\n\n\n{model} {model_scores}')
        values = [model_scores[model][metric] for metric in metrics]
        ax.bar(x + i * width, values, width, label=model)

    ax.set_title(f'Metriche per {uin}')
    ax.set_xticks(x + width)
    ax.set_xticklabels(metrics)
    ax.set_ylabel('Valore')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)

# Se ci sono assi vuoti, nascondili
for j in range(idx + 1, len(axs)):
    fig.delaxes(axs[j])

plt.tight_layout()
plt.show()


print(detail)

def plot_radar_charts(data):

    metrics = ['Precision@10', 'MAP', 'NDCG@10']
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    all_models = sorted(set(model for uin_scores in data.values() for model in uin_scores))

    num_uins = len(data)
    cols = 2
    rows = int(np.ceil(num_uins / cols))
    fig, axs = plt.subplots(rows, cols, subplot_kw=dict(polar=True), figsize=(cols * 6, rows * 6))
    axs = axs.flatten()

    for idx, (uin, model_scores) in enumerate(data.items()):
        ax = axs[idx]
        for model in all_models:
            values = [model_scores.get(model, {}).get(metric, np.nan) for metric in metrics]
            values += values[:1]
            ax.plot(angles, values, label=model)
            ax.fill(angles, values, alpha=0.1)

        ax.set_title(uin)
        ax.set_ylim(0, 1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    for j in range(idx + 1, len(axs)):
        fig.delaxes(axs[j])

    plt.suptitle('Radar Chart: Confronto Modelli per UIN', fontsize=16, y=1.05)
    plt.tight_layout()
    plt.show()

plot_radar_charts(detail)