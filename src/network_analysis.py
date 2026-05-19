import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
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

    filtered_G = G.copy()
    edges = list(filtered_G.edges(data='weight'))
    edges.sort(key=lambda x: x[2], reverse=True)
    if len(edges) > 45:
        edges = edges[:45]
        filtered_G = nx.Graph()
        for u, v, w in edges:
            filtered_G.add_edge(u, v, weight=w)

    deg = dict(filtered_G.degree())
    pos = nx.spring_layout(filtered_G, k=1.0, iterations=100, seed=42)

    fig, ax = plt.subplots(figsize=(14, 12), dpi=300, facecolor='white')
    ax.set_facecolor('white')

    edge_weights = [filtered_G[u][v]['weight'] for u, v in filtered_G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    
    for (u, v), w in zip(filtered_G.edges(), edge_weights):
        nx.draw_networkx_edges(filtered_G, pos, edgelist=[(u, v)],
                              width=0.5 + (w/max_weight)*1.2,
                              edge_color='#E8D5B7',
                              alpha=0.5,
                              ax=ax)

    node_sizes = [np.sqrt(deg.get(n, 1)) * 80 + 50 for n in filtered_G.nodes()]

    node_colors = ['#F4D03F' if deg[n] > 3 else '#C39BD3' for n in filtered_G.nodes()]

    for n in filtered_G.nodes():
        size = node_sizes[list(filtered_G.nodes()).index(n)]
        for i in range(3):
            alpha_val = 0.75 - i * 0.22
            size_factor = 1 - i * 0.28
            nx.draw_networkx_nodes(filtered_G, pos, nodelist=[n],
                                  node_size=size * size_factor,
                                  node_color=node_colors[list(filtered_G.nodes()).index(n)],
                                  alpha=alpha_val,
                                  linewidths=0,
                                  ax=ax)

    nx.draw_networkx_nodes(filtered_G, pos, node_size=[s*0.12 for s in node_sizes],
                          node_color='#000000',
                          alpha=0.65,
                          ax=ax)

    top_degree = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:10]
    label_dict = {n: n.split(',')[0].strip() for n, _ in top_degree}
    
    nx.draw_networkx_labels(filtered_G, pos, label_dict,
                           font_size=9,
                           font_weight='bold',
                           font_color='#5A4A42',
                           ax=ax,
                           bbox=dict(boxstyle="round,pad=0.3", 
                                     facecolor='#FEF9E7', 
                                     edgecolor='none', 
                                     alpha=0.9))

    ax.set_title('Author Collaboration Network', fontsize=16, fontweight='bold', pad=20, color='#333333')
    ax.axis('off')

    cbar_ax = fig.add_axes([0.15, 0.06, 0.7, 0.03])
    cmap = cm.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=2020, vmax=2026)
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), 
                        cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Publication Year', fontsize=11, fontweight='bold', labelpad=10)
    cbar.set_ticks([2020, 2021, 2022, 2023, 2024, 2025, 2026])
    cbar.set_ticklabels(['2020', '2021', '2022', '2023', '2024', '2025', '2026'])
    cbar.outline.set_visible(False)

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    
    output_file = os.path.join(output_dir, 'author_collaboration_network.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("Author collaboration network saved")


def build_institution_network():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    country_counts = df['Source Country'].dropna().value_counts().head(12)
    
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300, facecolor='white')
    
    colors = cm.viridis(np.linspace(0.2, 0.8, len(country_counts)))
    
    bars = ax.barh(range(len(country_counts)), country_counts.values,
                   color=colors, edgecolor='white', linewidth=0.8, height=0.7)
    
    ax.set_yticks(range(len(country_counts)))
    ax.set_yticklabels(country_counts.index, fontsize=11, fontweight='medium')
    ax.set_xlabel('Number of Publications', fontsize=12, fontweight='bold')
    ax.set_title('Research Output by Country', fontsize=15, fontweight='bold', pad=15, color='#333333')
    
    for i, (bar, count) in enumerate(zip(bars, country_counts.values)):
        ax.text(count + max(country_counts.values) * 0.008, bar.get_y() + bar.get_height()/2,
                str(int(count)), va='center', fontsize=10, fontweight='bold', color='#374151')
    
    ax.invert_yaxis()
    
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    
    ax.grid(axis='x', alpha=0.25, linestyle='--', color='#CCCCCC')
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'institution_country_network.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("Country distribution saved")


def build_cocitation_network():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    cocitation = defaultdict(int)
    
    for idx, row in df.iterrows():
        refs = str(row['References']).split(';') if pd.notna(row['References']) else []
        refs = [r.strip() for r in refs if r.strip() and r.strip() != 'nan'][:5]
        
        for i, ref1 in enumerate(refs):
            for j, ref2 in enumerate(refs):
                if i < j:
                    cocitation[(ref1, ref2)] += 1

    edges = [(ref1, ref2, count) for (ref1, ref2), count in cocitation.items() if count >= 2]
    edges.sort(key=lambda x: x[2], reverse=True)
    if len(edges) > 50:
        edges = edges[:50]
    
    G = nx.Graph()
    for ref1, ref2, count in edges:
        G.add_edge(ref1[:50], ref2[:50], weight=count)

    deg = dict(G.degree())
    pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

    fig, ax = plt.subplots(figsize=(14, 12), dpi=300, facecolor='white')
    ax.set_facecolor('white')

    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    
    for (u, v), w in zip(G.edges(), edge_weights):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                              width=0.4 + (w/max_weight)*1.0,
                              edge_color='#D4C4A8',
                              alpha=0.5,
                              ax=ax)

    node_sizes = [deg[n] * 30 + 40 for n in G.nodes()]
    node_colors = ['#87CEEB' if deg[n] > 2 else '#98FB98' for n in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                          node_color=node_colors,
                          alpha=0.7,
                          edgecolors='#FFFFFF',
                          linewidths=1.5,
                          ax=ax)

    top_degree = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:8]
    label_dict = {n: n[:20] + '..' if len(n) > 20 else n for n, _ in top_degree}
    
    nx.draw_networkx_labels(G, pos, label_dict,
                           font_size=8,
                           font_weight='bold',
                           font_color='#4A3728',
                           ax=ax,
                           bbox=dict(boxstyle="round,pad=0.25", 
                                     facecolor='#FFF8DC', 
                                     edgecolor='none', 
                                     alpha=0.9))

    ax.set_title('Co-citation Network', fontsize=16, fontweight='bold', pad=20, color='#333333')
    ax.axis('off')
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'citation_network.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("Co-citation network saved")


if __name__ == "__main__":
    build_keyword_cooccurrence()
    build_author_network()
    build_institution_network()
    build_cocitation_network()