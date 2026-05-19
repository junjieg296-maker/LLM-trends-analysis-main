import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def plot_publication_trend():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'expanded_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    print("Reading cleaned data: {}".format(data_path))

    df = pd.read_csv(data_path)
    year_col = 'Publication Year'

    if year_col not in df.columns:
        print("Cannot find year column '{}', please check CSV headers!".format(year_col))
        return

    year_counts = df[year_col].value_counts().sort_index().reset_index()
    year_counts.columns = ['Year', 'Count']

    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_theme(style="whitegrid")

    ax = sns.barplot(x='Year', y='Count', data=year_counts, palette='viridis', hue='Year', legend=False)

    sns.lineplot(x=range(len(year_counts)), y=year_counts['Count'], marker='o', color='red', linewidth=2)

    for p in ax.patches:
        ax.annotate('{}'.format(int(p.get_height())),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points',
                    fontsize=12, fontweight='bold')

    plt.title('Annual Publication Trend: LLM Multi-Agent Systems', fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Publications', fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    output_file = os.path.join(output_dir, 'publication_trend.png')
    plt.tight_layout()
    plt.savefig(output_file)
    print("Publication trend figure saved to: {}".format(output_file))
    plt.close()


if __name__ == "__main__":
    plot_publication_trend()