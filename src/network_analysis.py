import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
import textwrap
from collections import Counter, defaultdict
import matplotlib.colors as mcolors
import matplotlib.cm as cm


def split_clean_authors(author_cell):
    if pd.isna(author_cell):
        return []

    invalid_names = {"", "null", "null null", "nan", "none", "unknown"}
    authors = []
    for author in str(author_cell).split(';'):
        clean_author = " ".join(author.strip().split())
        if clean_author.lower() in invalid_names:
            continue
        authors.append(clean_author)
    return authors


def split_clean_references(reference_cell):
    if pd.isna(reference_cell):
        return []

    references = []
    seen = set()
    for reference in str(reference_cell).split(';'):
        clean_reference = " ".join(reference.strip().split())
        if not clean_reference or clean_reference.lower() == "nan":
            continue
        if clean_reference in seen:
            continue
        seen.add(clean_reference)
        references.append(clean_reference)
    return references


def shorten_title(title, max_chars=58):
    clean_title = " ".join(str(title).replace("\n", " ").split())
    if len(clean_title) <= max_chars:
        return clean_title
    return clean_title[: max_chars - 3].rstrip() + "..."


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
        authors = split_clean_authors(row['Author/s'])
        
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


def build_reference_cocitation_network(min_cited=2, max_nodes=36):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    corpus_ids = set(df['Lens ID'].dropna().astype(str).str.strip())
    id_to_meta = {}
    for _, row in df.iterrows():
        lens_id = str(row.get('Lens ID', '')).strip()
        if not lens_id:
            continue
        id_to_meta[lens_id] = {
            'title': str(row.get('Title', '')).strip(),
            'year': pd.to_numeric(row.get('Publication Year'), errors='coerce'),
            'citations': pd.to_numeric(row.get('Citing Works Count'), errors='coerce'),
            'source': str(row.get('Source Title', '')).strip(),
        }

    reference_counts = Counter()
    cocitation_counts = Counter()
    citing_years = defaultdict(list)

    for _, row in df.iterrows():
        publication_year = pd.to_numeric(row.get('Publication Year'), errors='coerce')
        references = [
            reference for reference in split_clean_references(row.get('References'))
            if reference in corpus_ids
        ]

        for reference in references:
            reference_counts[reference] += 1
            if not pd.isna(publication_year):
                citing_years[reference].append(int(publication_year))

        for i, ref_a in enumerate(references):
            for ref_b in references[i + 1:]:
                cocitation_counts[tuple(sorted((ref_a, ref_b)))] += 1

    selected_references = [
        reference for reference, count in reference_counts.most_common(max_nodes)
        if count >= min_cited
    ]

    G = nx.Graph()
    for reference in selected_references:
        meta = id_to_meta.get(reference, {})
        year = meta.get('year', np.nan)
        avg_citing_year = np.mean(citing_years[reference]) if citing_years[reference] else np.nan
        G.add_node(
            reference,
            count=reference_counts[reference],
            title=meta.get('title', reference),
            year=int(year) if not pd.isna(year) else None,
            avg_citing_year=float(avg_citing_year) if not pd.isna(avg_citing_year) else None,
            source=meta.get('source', ''),
        )

    for (ref_a, ref_b), weight in cocitation_counts.items():
        if ref_a in G and ref_b in G and weight >= 1:
            G.add_edge(ref_a, ref_b, weight=weight)

    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    print(
        f"Reference co-citation network built: "
        f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
    )

    if G.number_of_nodes() == 0:
        print("No co-citation network generated because no internal co-cited references met the threshold.")
        return G

    communities = list(nx.algorithms.community.greedy_modularity_communities(G, weight='weight'))
    communities = sorted(communities, key=len, reverse=True)
    cluster_lookup = {}
    for cluster_id, community in enumerate(communities):
        for node in community:
            cluster_lookup[node] = cluster_id

    palette = [
        '#2F6F9F',
        '#D66A4A',
        '#3B9C8A',
        '#C99A2E',
        '#8B5A8C',
        '#5A8F55',
        '#7C6F64',
        '#4B778D',
    ]
    node_colors = [palette[cluster_lookup.get(node, 0) % len(palette)] for node in G.nodes()]
    node_counts = np.array([G.nodes[node]['count'] for node in G.nodes()], dtype=float)
    max_count = node_counts.max() if len(node_counts) else 1
    node_sizes = 250 + 1850 * np.sqrt(node_counts / max_count)

    max_edge_weight = max([data['weight'] for _, _, data in G.edges(data=True)] or [1])
    edge_widths = [0.75 + 3.2 * data['weight'] / max_edge_weight for _, _, data in G.edges(data=True)]
    edge_alpha = [0.18 + 0.42 * data['weight'] / max_edge_weight for _, _, data in G.edges(data=True)]

    pos = nx.spring_layout(G, k=0.95, iterations=250, seed=24, weight='weight')

    fig = plt.figure(figsize=(16, 10), dpi=260, facecolor='#FAF9F5')
    ax = fig.add_axes([0.035, 0.08, 0.68, 0.78])
    side = fig.add_axes([0.74, 0.10, 0.23, 0.76])
    ax.set_facecolor('#FAF9F5')
    side.set_facecolor('#FAF9F5')

    fig.text(
        0.04,
        0.94,
        'Reference Co-citation Network',
        fontsize=24,
        fontweight='bold',
        color='#26323B',
        ha='left',
    )
    fig.text(
        0.04,
        0.905,
        'CiteSpace-style backbone built from shared cited references in the 522-record Lens.org corpus',
        fontsize=12.5,
        color='#667682',
        ha='left',
    )
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.885, 0.885], color='#DADDD6', linewidth=1.4))

    for (u, v, data), width, alpha in zip(G.edges(data=True), edge_widths, edge_alpha):
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            width=width,
            edge_color='#9CAAAE',
            alpha=alpha,
            ax=ax,
        )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes * 1.55,
        node_color=node_colors,
        alpha=0.16,
        linewidths=0,
        ax=ax,
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.88,
        edgecolors='white',
        linewidths=1.8,
        ax=ax,
    )

    degree_weight = dict(G.degree(weight='weight'))
    label_nodes = sorted(
        G.nodes(),
        key=lambda node: (G.nodes[node]['count'], degree_weight.get(node, 0)),
        reverse=True,
    )[:14]
    for node in label_nodes:
        x, y = pos[node]
        title = shorten_title(G.nodes[node]['title'], 48)
        label = "\n".join(textwrap.wrap(title, width=23)[:2])
        ax.annotate(
            label,
            (x, y),
            xytext=(7, 7),
            textcoords='offset points',
            fontsize=6.8,
            color='#26323B',
            ha='left',
            va='bottom',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='none', alpha=0.82),
        )

    ax.axis('off')

    top_nodes = sorted(G.nodes(), key=lambda node: G.nodes[node]['count'], reverse=True)[:8]
    side.axis('off')
    side.text(0.0, 0.97, 'Top co-cited anchors', fontsize=13, fontweight='bold', color='#26323B')
    side.text(0.0, 0.925, 'Count = times cited by papers in this corpus', fontsize=8.6, color='#667682')
    y = 0.865
    for rank, node in enumerate(top_nodes, 1):
        color = palette[cluster_lookup.get(node, 0) % len(palette)]
        count = G.nodes[node]['count']
        year = G.nodes[node]['year'] or 'n/a'
        title = shorten_title(G.nodes[node]['title'], 55)
        side.scatter([0.015], [y + 0.009], s=70, color=color, edgecolors='white', linewidths=0.8)
        side.text(0.045, y + 0.018, f'#{rank}  n={count}  year={year}', fontsize=8.8, color=color, fontweight='bold')
        wrapped = textwrap.wrap(title, width=34)[:2]
        side.text(0.045, y - 0.006, "\n".join(wrapped), fontsize=8.2, color='#26323B', va='top')
        y -= 0.086

    side.text(0.0, y - 0.02, 'Reading guide', fontsize=13, fontweight='bold', color='#26323B')
    guide_items = [
        ('Node size', 'citation frequency within the corpus'),
        ('Edge width', 'co-citation strength'),
        ('Color', 'network community detected from weighted links'),
        ('Scope', 'only cited references also present in the corpus are labeled'),
    ]
    y -= 0.065
    for head, body in guide_items:
        side.text(0.0, y, head, fontsize=9, color='#26323B', fontweight='bold')
        side.text(0.18, y, body, fontsize=8.5, color='#667682')
        y -= 0.052

    side.text(0.0, 0.035, f'Network: {G.number_of_nodes()} nodes / {G.number_of_edges()} edges', fontsize=8.8, color='#667682')
    side.text(0.0, 0.005, 'Data source: cleaned Lens.org records, 2020-2026', fontsize=8.8, color='#667682')

    output_file = os.path.join(output_dir, 'reference_cocitation_network.png')
    plt.savefig(output_file, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Reference co-citation network saved to: {output_file}")

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
    build_reference_cocitation_network()
    build_reference_citation_network()
