import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
from collections import defaultdict
import matplotlib.colors as mcolors
import matplotlib.cm as cm


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
    if len(edges) > 45:
        edges = edges[:45]
    
    G = nx.Graph()
    for kw1, kw2, count in edges:
        G.add_edge(kw1, kw2, weight=count)

    for kw, count in keyword_counts.items():
        if kw in G.nodes():
            G.nodes[kw]['count'] = count

    deg = dict(G.degree())
    pos = nx.spring_layout(G, k=1.2, iterations=100, seed=42)

    fig, ax = plt.subplots(figsize=(14, 12), dpi=300, facecolor='white')
    ax.set_facecolor('white')

    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    
    for (u, v), w in zip(G.edges(), edge_weights):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                              width=0.5 + (w/max_weight)*1.0,
                              edge_color='#C7B2B2',
                              alpha=0.45,
                              ax=ax)

    node_sizes = [np.sqrt(G.nodes[n].get('count', 1)) * 30 + 60 for n in G.nodes()]
    
    years_colors = {
        2020: '#1E3A5F',
        2021: '#2E5A7B',
        2022: '#4A8C9E',
        2023: '#C4A77D',
        2024: '#D4A574',
        2025: '#DF986C',
        2026: '#E8856A'
    }
    
    avg_year = 2023
    node_colors = ['#DF986C' if deg[n] > 3 else '#C4A77D' for n in G.nodes()]

    for n in G.nodes():
        size = node_sizes[list(G.nodes()).index(n)]
        for i in range(3):
            alpha_val = 0.8 - i * 0.25
            size_factor = 1 - i * 0.3
            nx.draw_networkx_nodes(G, pos, nodelist=[n],
                                  node_size=size * size_factor,
                                  node_color=node_colors[list(G.nodes()).index(n)],
                                  alpha=alpha_val,
                                  linewidths=0,
                                  ax=ax)

    nx.draw_networkx_nodes(G, pos, node_size=[s*0.15 for s in node_sizes],
                          node_color='#000000',
                          alpha=0.7,
                          ax=ax)

    top_degree = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:12]
    label_dict = {n: n.replace('_', ' ').title() for n, _ in top_degree}
    
    nx.draw_networkx_labels(G, pos, label_dict,
                           font_size=9,
                           font_weight='bold',
                           font_color='#5A4A42',
                           ax=ax,
                           bbox=dict(boxstyle="round,pad=0.3", 
                                     facecolor='#F5E6C8', 
                                     edgecolor='none', 
                                     alpha=0.9))

    ax.set_title('Keyword Co-occurrence Network', fontsize=16, fontweight='bold', pad=20, color='#333333')
    ax.axis('off')

    cbar_ax = fig.add_axes([0.15, 0.06, 0.7, 0.03])
    cmap = cm.get_cmap('coolwarm_r')
    norm = mcolors.Normalize(vmin=2020, vmax=2026)
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), 
                        cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Publication Year', fontsize=11, fontweight='bold', labelpad=10)
    cbar.set_ticks([2020, 2021, 2022, 2023, 2024, 2025, 2026])
    cbar.set_ticklabels(['2020', '2021', '2022', '2023', '2024', '2025', '2026'])
    cbar.outline.set_visible(False)

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    
    output_file = os.path.join(output_dir, 'keyword_cooccurrence_network.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("Keyword co-occurrence network saved")


def build_author_network():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    G = nx.Graph()
    
    for idx, row in df.iterrows():
        authors = str(row['Author/s']).split(';') if pd.notna(row['Author/s']) else []
        authors = [a.strip() for a in authors if a.strip()]
        
        for i, author1 in enumerate(authors):
            for j, author2 in enumerate(authors):
                if i < j:
                    if G.has_edge(author1, author2):
                        G[author1][author2]['weight'] += 1
                    else:
                        G.add_edge(author1, author2, weight=1)

    print(f"作者合作网络构建完成: {G.number_of_nodes()}个节点, {G.number_of_edges()}条边")

    filtered_G = G.copy()
    edges_to_remove = [(u, v) for u, v, w in filtered_G.edges(data='weight') if w < 2]
    filtered_G.remove_edges_from(edges_to_remove)
    filtered_G.remove_nodes_from(list(nx.isolates(filtered_G)))
    
    print(f"过滤后(合作>=2次): {filtered_G.number_of_nodes()}个节点, {filtered_G.number_of_edges()}条边")

    pos = nx.spring_layout(filtered_G, k=0.15, iterations=50)
    
    plt.figure(figsize=(16, 12), dpi=300)
    
    edge_weights = [filtered_G[u][v]['weight'] for u, v in filtered_G.edges()]
    nx.draw_networkx_edges(filtered_G, pos, width=[w*0.5 for w in edge_weights], 
                           edge_color='lightblue', alpha=0.6)
    
    node_sizes = [nx.degree(filtered_G, n) * 50 for n in filtered_G.nodes()]
    nx.draw_networkx_nodes(filtered_G, pos, node_size=node_sizes, 
                          node_color='orange', alpha=0.8)

    high_degree_nodes = [n for n in filtered_G.nodes() if nx.degree(filtered_G, n) >= 3]
    nx.draw_networkx_labels(filtered_G, pos, 
                           labels={n: n for n in high_degree_nodes},
                           font_size=8, font_weight='bold')

    plt.title('Author Collaboration Network (LLM Multi-Agent Research)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'author_collaboration_network.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"作者合作网络图已保存至: {output_file}")
    
    return G


def build_institution_network():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    G = nx.Graph()
    
    for idx, row in df.iterrows():
        source_country = str(row['Source Country']).strip() if pd.notna(row['Source Country']) else "Unknown"
        if source_country and source_country != "nan":
            G.add_node(source_country, type='country')
    
    country_counts = df['Source Country'].dropna().value_counts()
    for country, count in country_counts.items():
        if G.has_node(country.strip()):
            G.nodes[country.strip()]['papers'] = count

    plt.figure(figsize=(14, 10), dpi=300)
    pos = nx.kamada_kawai_layout(G)
    
    node_sizes = [G.nodes[n].get('papers', 1) * 10 for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color='green', alpha=0.7)
    
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

    plt.title('Research Institutions Country Distribution', 
              fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'institution_country_network.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"机构国家分布图已保存至: {output_file}")
    
    return G


def build_reference_citation_network():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    G = nx.DiGraph()
    
    for idx, row in df.iterrows():
        paper_id = row['Lens ID']
        references = str(row['References']).split(';') if pd.notna(row['References']) else []
        references = [r.strip() for r in references if r.strip() and r.strip() != "nan"]
        
        G.add_node(paper_id, type='paper', title=str(row['Title'])[:50])
        
        for ref_id in references[:10]:
            G.add_edge(paper_id, ref_id, type='cites')

    print(f"引用网络构建完成: {G.number_of_nodes()}个节点, {G.number_of_edges()}条边")

    plt.figure(figsize=(14, 10), dpi=300)
    pos = nx.spring_layout(G, k=0.2)
    
    node_colors = ['red' if G.nodes[n].get('type') == 'paper' else 'blue' for n in G.nodes()]
    node_sizes = [50 if G.nodes[n].get('type') == 'paper' else 20 for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color=node_colors, alpha=0.6)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, arrows=True)

    plt.title('Citation Reference Network (Simplified)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'citation_network.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"引用网络图已保存至: {output_file}")
    
    return G


if __name__ == "__main__":
    build_author_network()
    build_institution_network()
    build_reference_citation_network()
