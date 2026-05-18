import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os


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