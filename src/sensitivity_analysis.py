import pandas as pd
import numpy as np
import os
import networkx as nx


def run_sensitivity_analysis():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'expanded_data.csv')
    output_dir = os.path.join(base_path, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    results = []

    # --- 1. 关键词共现阈值敏感性 ---
    print("测试关键词共现阈值敏感性...")
    thresholds = [1, 2, 3, 4, 5, 10]
    for threshold in thresholds:
        cooccurrence = {}
        for idx, row in df.iterrows():
            keywords = str(row['Keywords']).split(';') if pd.notna(row['Keywords']) else []
            keywords = [k.strip().lower() for k in keywords if k.strip() and len(k.strip()) > 2]
            for i, kw1 in enumerate(keywords):
                for j, kw2 in enumerate(keywords):
                    if i < j:
                        key = tuple(sorted([kw1, kw2]))
                        cooccurrence[key] = cooccurrence.get(key, 0) + 1
        
        edges_above_thresh = sum(1 for v in cooccurrence.values() if v >= threshold)
        unique_kws = set()
        for (kw1, kw2), cnt in cooccurrence.items():
            if cnt >= threshold:
                unique_kws.add(kw1)
                unique_kws.add(kw2)
        
        results.append({
            'analysis_type': 'keyword_cooccurrence',
            'parameter': 'threshold',
            'value': threshold,
            'edges': edges_above_thresh,
            'nodes': len(unique_kws)
        })

    # --- 2. 作者合作阈值敏感性 ---
    print("测试作者合作阈值敏感性...")
    for threshold in [1, 2, 3, 5, 10]:
        author_pairs = {}
        for idx, row in df.iterrows():
            authors = str(row['Author/s']).split(';') if pd.notna(row['Author/s']) else []
            authors = [a.strip() for a in authors if a.strip()]
            for i, a1 in enumerate(authors):
                for j, a2 in enumerate(authors):
                    if i < j:
                        key = tuple(sorted([a1, a2]))
                        author_pairs[key] = author_pairs.get(key, 0) + 1
        
        edges_above = sum(1 for v in author_pairs.values() if v >= threshold)
        unique_authors = set()
        for (a1, a2), cnt in author_pairs.items():
            if cnt >= threshold:
                unique_authors.add(a1)
                unique_authors.add(a2)
        
        results.append({
            'analysis_type': 'author_collaboration',
            'parameter': 'threshold',
            'value': threshold,
            'edges': edges_above,
            'nodes': len(unique_authors)
        })

    # --- 3. 时间窗口敏感性 ---
    print("测试时间窗口敏感性...")
    year_windows = [[2020, 2023], [2021, 2024], [2022, 2025], [2023, 2026], [2020, 2026]]
    for window in year_windows:
        start, end = window
        filtered = df[(df['Publication Year'] >= start) & (df['Publication Year'] <= end)]
        citing_mean = filtered['Citing Works Count'].dropna().mean()
        h_index = calculate_h_index(filtered['Citing Works Count'].dropna().astype(int))
        
        results.append({
            'analysis_type': 'time_window',
            'parameter': f"{start}-{end}",
            'value': len(filtered),
            'avg_citations': citing_mean,
            'h_index': h_index
        })

    # --- 4. 节点过滤敏感性 ---
    print("测试节点度过滤敏感性...")
    degree_thresholds = [1, 2, 3, 5, 10]
    G = nx.Graph()
    for idx, row in df.iterrows():
        authors = str(row['Author/s']).split(';') if pd.notna(row['Author/s']) else []
        authors = [a.strip() for a in authors if a.strip()]
        for i, a1 in enumerate(authors):
            for j, a2 in enumerate(authors):
                if i < j:
                    if G.has_edge(a1, a2):
                        G[a1][a2]['weight'] += 1
                    else:
                        G.add_edge(a1, a2, weight=1)
    
    for threshold in degree_thresholds:
        filtered_G = G.copy()
        nodes_to_remove = [n for n in filtered_G.nodes() if filtered_G.degree(n) < threshold]
        filtered_G.remove_nodes_from(nodes_to_remove)
        
        if filtered_G.number_of_nodes() > 0:
            avg_clustering = nx.average_clustering(filtered_G)
            if nx.is_connected(filtered_G):
                avg_shortest_path = nx.average_shortest_path_length(filtered_G)
            else:
                avg_shortest_path = 0
        else:
            avg_clustering = 0
            avg_shortest_path = 0
        
        results.append({
            'analysis_type': 'degree_filter',
            'parameter': 'min_degree',
            'value': threshold,
            'nodes': filtered_G.number_of_nodes(),
            'edges': filtered_G.number_of_edges(),
            'avg_clustering': avg_clustering,
            'avg_path_length': avg_shortest_path
        })

    # --- 输出敏感性分析报告 ---
    output_file = os.path.join(output_dir, 'sensitivity_analysis_report.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("        LLM多智能体领域参数敏感性分析报告\n")
        f.write("=" * 60 + "\n\n")

        f.write("【一、关键词共现阈值敏感性】\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'阈值':>6} {'边数':>8} {'节点数':>8}\n")
        f.write("-" * 40 + "\n")
        for r in [x for x in results if x['analysis_type'] == 'keyword_cooccurrence']:
            f.write(f"{r['value']:>6} {r['edges']:>8} {r['nodes']:>8}\n")
        f.write("\n")

        f.write("【二、作者合作阈值敏感性】\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'阈值':>6} {'边数':>8} {'节点数':>8}\n")
        f.write("-" * 40 + "\n")
        for r in [x for x in results if x['analysis_type'] == 'author_collaboration']:
            f.write(f"{r['value']:>6} {r['edges']:>8} {r['nodes']:>8}\n")
        f.write("\n")

        f.write("【三、时间窗口敏感性】\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'时间窗口':>12} {'文献数':>8} {'篇均被引':>10} {'h指数':>6}\n")
        f.write("-" * 40 + "\n")
        for r in [x for x in results if x['analysis_type'] == 'time_window']:
            f.write(f"{r['parameter']:>12} {r['value']:>8} {r['avg_citations']:>10.2f} {r['h_index']:>6}\n")
        f.write("\n")

        f.write("【四、节点度过滤敏感性】\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'最小度':>6} {'节点数':>8} {'边数':>8} {'聚类系数':>12} {'平均路径':>12}\n")
        f.write("-" * 55 + "\n")
        for r in [x for x in results if x['analysis_type'] == 'degree_filter']:
            f.write(f"{r['value']:>6} {r['nodes']:>8} {r['edges']:>8} {r['avg_clustering']:>12.4f} {r['avg_path_length']:>12.4f}\n")

    print(f"参数敏感性分析报告已保存至: {output_file}")
    return results


def calculate_h_index(citations):
    sorted_citations = np.sort(np.array(list(citations)))[::-1]
    h_index = sum(i + 1 <= sorted_citations[i] for i in range(len(sorted_citations)))
    return h_index


if __name__ == "__main__":
    run_sensitivity_analysis()