import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def plot_publication_trend():
    # 1. 自动定位路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    print(f"🚀 正在读取清洗后的数据: {data_path}")

    # 2. 读取并处理年份数据
    df = pd.read_csv(data_path)
    # Lens.org 的年份列名通常是 'Publication Year'
    year_col = 'Publication Year'

    if year_col not in df.columns:
        print(f"❌ 找不到年份列 '{year_col}'，请检查 CSV 表头！")
        return

    # 统计每年的发文量并排序
    year_counts = df[year_col].value_counts().sort_index().reset_index()
    year_counts.columns = ['Year', 'Count']

    # 3. 开始绘图（高质量设置）
    plt.figure(figsize=(10, 6), dpi=300)  # 设置 300 DPI 高清分辨率
    sns.set_theme(style="whitegrid")  # 设置高级白色网格主题

    # 画柱状图
    ax = sns.barplot(x='Year', y='Count', data=year_counts, palette='viridis', hue='Year', legend=False)

    # 画折线图（增加动感）
    sns.lineplot(x=range(len(year_counts)), y=year_counts['Count'], marker='o', color='red', linewidth=2)

    # 在柱子上方标注具体的数字
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points',
                    fontsize=12, fontweight='bold')

    # 4. 润色图表标签
    plt.title('Annual Publication Trend: LLM Multi-Agent Systems', fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Publications', fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    # 5. 保存并展示
    output_file = os.path.join(output_dir, 'publication_trend.png')
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"✅ 高质量趋势图已保存至: {output_file}")
    plt.show()


if __name__ == "__main__":
    plot_publication_trend()