import pandas as pd
import numpy as np
import os
from scipy import stats


def calculate_metrics():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'expanded_data.csv')
    output_dir = os.path.join(base_path, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    metrics = {}

    year_counts = df['Publication Year'].value_counts().sort_index()

    growth_rates = []
    for i in range(1, len(year_counts)):
        prev = year_counts.iloc[i-1]
        curr = year_counts.iloc[i]
        if prev > 0:
            rate = (curr - prev) / prev * 100
            growth_rates.append(rate)

    metrics['annual_publications'] = year_counts.to_dict()
    metrics['avg_growth_rate'] = np.mean(growth_rates) if growth_rates else 0
    metrics['growth_rate_std'] = np.std(growth_rates) if growth_rates else 0

    citing_works = df['Citing Works Count'].dropna().astype(int)
    metrics['total_citations'] = int(citing_works.sum())
    metrics['avg_citations'] = float(citing_works.mean())
    metrics['median_citations'] = float(citing_works.median())
    metrics['highly_cited'] = int((citing_works > 50).sum())
    metrics['zero_citations'] = int((citing_works == 0).sum())

    sorted_citations = np.sort(citing_works)[::-1]
    h_index = sum(i + 1 <= sorted_citations[i] for i in range(len(sorted_citations)))
    metrics['h_index'] = h_index

    journal_counts = df['Source Title'].value_counts().head(10)
    metrics['top_journals'] = journal_counts.to_dict()

    type_counts = df['Publication Type'].value_counts()
    metrics['doc_types'] = type_counts.to_dict()

    open_access = df['Is Open Access'].dropna()
    open_access_ratio = sum(1 for val in open_access if str(val).lower() == 'yes') / len(open_access) * 100
    metrics['open_access_ratio'] = float(open_access_ratio)

    all_authors = []
    for authors in df['Author/s'].dropna().astype(str):
        all_authors.extend([a.strip() for a in authors.split(';')])
    author_counts = pd.Series(all_authors).value_counts().head(10)
    metrics['top_authors'] = author_counts.to_dict()
    metrics['total_authors'] = len(set(all_authors))
    metrics['avg_authors_per_paper'] = df['Author/s'].dropna().apply(lambda x: len([a.strip() for a in x.split(';')])).mean()

    fields = []
    for field in df['Fields of Study'].dropna().astype(str):
        fields.extend([f.strip() for f in field.split(';')])
    field_counts = pd.Series(fields).value_counts().head(15)
    metrics['top_fields'] = field_counts.to_dict()

    output_file = os.path.join(output_dir, 'metrics_summary.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("            LLM Multi-Agent Bibliometric Analysis Report\n")
        f.write("=" * 60 + "\n\n")

        f.write("【1. Temporal Metrics】\n")
        f.write("-" * 40 + "\n")
        for year, count in metrics['annual_publications'].items():
            f.write("  {}: {} papers\n".format(int(year), count))
        f.write("\n  Average Annual Growth Rate: {:.2f}%\n".format(metrics['avg_growth_rate']))
        f.write("  Growth Rate Std: {:.2f}%\n\n".format(metrics['growth_rate_std']))

        f.write("【2. Impact Metrics】\n")
        f.write("-" * 40 + "\n")
        f.write("  Total Citations: {:,}\n".format(metrics['total_citations']))
        f.write("  Average Citations per Paper: {:.2f}\n".format(metrics['avg_citations']))
        f.write("  Median Citations: {:.2f}\n".format(metrics['median_citations']))
        f.write("  Highly Cited Papers (>50 citations): {}\n".format(metrics['highly_cited']))
        f.write("  Zero Citation Papers: {}\n".format(metrics['zero_citations']))
        f.write("  h-index: {}\n\n".format(metrics['h_index']))

        f.write("【3. Top 10 Journals】\n")
        f.write("-" * 40 + "\n")
        for journal, count in metrics['top_journals'].items():
            f.write("  {}: {} papers\n".format(journal, count))
        f.write("\n")

        f.write("【4. Document Type Distribution】\n")
        f.write("-" * 40 + "\n")
        for doc_type, count in metrics['doc_types'].items():
            f.write("  {}: {} papers ({:.1f}%)\n".format(doc_type, count, count/len(df)*100))
        f.write("\n")

        f.write("【5. Open Access Status】\n")
        f.write("-" * 40 + "\n")
        f.write("  Open Access Ratio: {:.2f}%\n\n".format(metrics['open_access_ratio']))

        f.write("【6. Author Statistics】\n")
        f.write("-" * 40 + "\n")
        f.write("  Total Authors: {:,}\n".format(metrics['total_authors']))
        f.write("  Average Authors per Paper: {:.2f}\n".format(metrics['avg_authors_per_paper']))
        f.write("\n  Top 10 Prolific Authors:\n")
        for author, count in metrics['top_authors'].items():
            f.write("    {}: {} papers\n".format(author, count))
        f.write("\n")

        f.write("【7. Top 15 Research Fields】\n")
        f.write("-" * 40 + "\n")
        for field, count in metrics['top_fields'].items():
            f.write("  {}: {} occurrences\n".format(field, count))

    print("Metrics analysis report saved to: {}".format(output_file))
    return metrics


if __name__ == "__main__":
    calculate_metrics()