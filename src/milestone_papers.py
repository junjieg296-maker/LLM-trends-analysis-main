import os

import pandas as pd


def build_milestone_candidates(top_n=10):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    columns = [
        'Title',
        'Publication Year',
        'Source Title',
        'Author/s',
        'Citing Works Count',
        'DOI',
        'Fields of Study',
    ]
    available_columns = [column for column in columns if column in df.columns]
    candidates = df[available_columns].copy()
    candidates['Citing Works Count'] = pd.to_numeric(
        candidates['Citing Works Count'], errors='coerce'
    ).fillna(0).astype(int)
    candidates = candidates.sort_values(
        ['Citing Works Count', 'Publication Year'], ascending=[False, True]
    ).head(top_n)

    output_csv = os.path.join(output_dir, 'milestone_paper_candidates.csv')
    candidates.to_csv(output_csv, index=False, encoding='utf-8-sig')

    output_md = os.path.join(output_dir, 'milestone_paper_candidates.md')
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("# Top 10 Milestone Paper Candidates\n\n")
        f.write(
            "Selection rule: papers are ranked by Lens.org citing works count. "
            "This table is a first-pass milestone candidate list and should be "
            "combined with burst, centrality, and cluster-position evidence when "
            "CiteSpace/VOSviewer results are available.\n\n"
        )
        f.write("| Rank | Year | Citations | Title | Source | DOI |\n")
        f.write("|---:|---:|---:|---|---|---|\n")
        for rank, (_, row) in enumerate(candidates.iterrows(), 1):
            title = str(row.get('Title', '')).replace('|', '/')
            source = str(row.get('Source Title', '')).replace('|', '/')
            doi = str(row.get('DOI', '')).replace('|', '/')
            year = row.get('Publication Year', '')
            citations = row.get('Citing Works Count', 0)
            f.write(f"| {rank} | {year} | {citations} | {title} | {source} | {doi} |\n")

    print(f"Milestone candidates saved to: {output_csv}")
    print(f"Milestone candidate table saved to: {output_md}")
    return candidates


if __name__ == "__main__":
    build_milestone_candidates()
