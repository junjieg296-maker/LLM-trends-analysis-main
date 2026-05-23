import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from collections import defaultdict


def normalize_keywords(raw_keywords):
    """Normalize and de-duplicate keywords within one paper before counting pairs."""
    if pd.isna(raw_keywords):
        return []

    seen = set()
    normalized = []
    for keyword in str(raw_keywords).split(';'):
        clean_keyword = " ".join(keyword.strip().lower().split())
        if len(clean_keyword) <= 2 or clean_keyword in seen:
            continue
        seen.add(clean_keyword)
        normalized.append(clean_keyword)
    return normalized


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
        keywords = normalize_keywords(row['Keywords'])
        
        if len(keywords) < 2:
            continue
        
        for i, kw1 in enumerate(keywords):
            keyword_counts[kw1] += 1
            for j, kw2 in enumerate(keywords):
                if i < j:
                    cooccurrence[(kw1, kw2)] += 1

    G = nx.Graph()
    
    for (kw1, kw2), count in cooccurrence.items():
        if count >= 2:
            G.add_edge(kw1, kw2, weight=count)

    for kw, count in keyword_counts.items():
        if kw in G.nodes():
            G.nodes[kw]['count'] = count

    print(f"关键词共现网络构建完成: {G.number_of_nodes()}个节点, {G.number_of_edges()}条边")

    plt.figure(figsize=(18, 14), dpi=300)
    
    pos = nx.spring_layout(G, k=0.25, iterations=60)
    
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w*0.8 for w in edge_weights], 
                           edge_color='purple', alpha=0.5)
    
    node_sizes = [G.nodes[n].get('count', 1) * 30 for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color='yellow', alpha=0.8, edgecolors='black')

    label_threshold = 3
    labels = {n: n for n in G.nodes() if G.nodes[n].get('count', 1) >= label_threshold}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')

    plt.title('Keyword Co-occurrence Network (LLM Multi-Agent Research)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'keyword_cooccurrence_network.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"关键词共现网络图已保存至: {output_file}")

    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    output_file_txt = os.path.join(base_path, 'outputs', 'keyword_statistics.txt')
    with open(output_file_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("        LLM多智能体领域关键词统计报告\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("【TOP20 高频关键词】\n")
        f.write("-" * 40 + "\n")
        for i, (kw, count) in enumerate(top_keywords, 1):
            f.write(f"{i:2d}. {kw:25} {count:4d}次\n")
        
        f.write("\n【关键词共现关系(共现>=2次)】\n")
        f.write("-" * 40 + "\n")
        sorted_cooccur = sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:30]
        for (kw1, kw2), count in sorted_cooccur:
            if count >= 2 and kw1 != kw2:
                f.write(f"{kw1:20} ↔ {kw2:20} 共现{count}次\n")

    print(f"关键词统计报告已保存至: {output_file_txt}")
    
    return G


if __name__ == "__main__":
    build_keyword_cooccurrence()
