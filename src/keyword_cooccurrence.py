import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import os
import numpy as np
from collections import defaultdict


def build_keyword_cooccurrence():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    cooccurrence = defaultdict(int)
    keyword_counts = defaultdict(int)

    for idx, row in df.iterrows():
        keywords = str(row['Keywords']).split(';') if pd.notna(row['Keywords']) else []
        keywords = [k.strip().lower() for k in keywords if k.strip() and len(k.strip()) > 2]
        
        if len(keywords) < 2:
            continue
        
        for i, kw1 in enumerate(keywords):
            keyword_counts[kw1] += 1
            for j, kw2 in enumerate(keywords):
                if i < j:
                    cooccurrence[(kw1, kw2)] += 1

    edges = [(kw1, kw2, count) for (kw1, kw2), count in cooccurrence.items() if count >= 5]
    edges.sort(key=lambda x: x[2], reverse=True)
    if len(edges) > 40:
        edges = edges[:40]
    
    G = nx.Graph()
    for kw1, kw2, count in edges:
        G.add_edge(kw1, kw2, weight=count)

    for kw, count in keyword_counts.items():
        if kw in G.nodes():
            G.nodes[kw]['count'] = count

    print("Keyword co-occurrence network: {} nodes, {} edges".format(G.number_of_nodes(), G.number_of_edges()))

    fig, ax = plt.subplots(figsize=(14, 12), dpi=300, facecolor='#FAFBFC')
    ax.set_facecolor('#FAFBFC')
    
    pos = nx.spring_layout(G, k=2.0, iterations=120, seed=42)
    
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    
    for (u, v), w in zip(G.edges(), edge_weights):
        alpha_val = 0.12 + (w / max_weight) * 0.38
        width_val = 0.5 + (w / max_weight) * 2.0
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], 
                               width=width_val, edge_color='#059669',
                               alpha=alpha_val, ax=ax, connectionstyle="arc3,rad=0.05")
    
    degree_values = [G.degree(n) for n in G.nodes()]
    max_degree = max(degree_values) if degree_values else 1
    
    node_sizes = [300 + (G.degree(n) / max_degree) ** 0.85 * 1400 for n in G.nodes()]
    
    colors_kw = ['#059669', '#10B981', '#6EE7B7']
    node_colors = []
    for n in G.nodes():
        ratio = G.degree(n) / max_degree
        if ratio >= 0.55:
            node_colors.append(colors_kw[0])
        elif ratio >= 0.25:
            node_colors.append(colors_kw[1])
        else:
            node_colors.append(colors_kw[2])
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color=node_colors, alpha=0.92,
                          edgecolors='white', linewidths=2.5, ax=ax)

    top_nodes = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    labels = {n: n.replace('-', ' ').replace('_', ' ').title() 
              for n, _ in top_nodes if n in G.nodes()}
    
    nx.draw_networkx_labels(
        G, pos, labels, font_size=10, font_weight='600',
        font_color='#064E3B', ax=ax,
        bbox=dict(boxstyle="round,pad=0.35", facecolor='white', 
                  edgecolor='#A7F3D0', linewidth=1.2, alpha=0.95),
        horizontalalignment='center'
    )

    ax.set_title('Keyword Co-occurrence Network', fontsize=20, fontweight='700',
                 pad=22, color='#064E3B', loc='left')
    ax.axis('off')
    
    fig.patch.set_facecolor('#FAFBFC')
    plt.tight_layout(pad=1.5)
    
    output_file = os.path.join(output_dir, 'keyword_cooccurrence_network.png')
    fig.savefig(output_file, bbox_inches='tight', facecolor='#FAFBFC', dpi=300, pad_inches=0.15)
    print("Keyword co-occurrence network saved to: {}".format(output_file))
    plt.close(fig)

    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    output_file_txt = os.path.join(base_path, 'outputs', 'keyword_statistics.txt')
    with open(output_file_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("        LLM Multi-Agent Keyword Statistics Report\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("【TOP20 Keywords】\n")
        f.write("-" * 40 + "\n")
        for i, (kw, count) in enumerate(top_keywords, 1):
            f.write("{:2d}. {:25} {:4d} occurrences\n".format(i, kw, count))
        
        f.write("\n【Keyword Co-occurrence (>=5)】\n")
        f.write("-" * 40 + "\n")
        sorted_cooccur = sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:30]
        for (kw1, kw2), count in sorted_cooccur:
            if count >= 5:
                f.write("{:20} <-> {:20} co-occurred {} times\n".format(kw1, kw2, count))

    print("Keyword statistics saved to: {}".format(output_file_txt))
    
    return G


if __name__ == "__main__":
    build_keyword_cooccurrence()
