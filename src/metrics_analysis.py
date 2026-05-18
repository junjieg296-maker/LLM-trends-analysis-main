import pandas as pd
import numpy as np
import os
from scipy import stats


def calculate_metrics():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    metrics = {}

    # --- 1. 时间维度指标 ---
    year_counts = df['Publication Year'].value_counts().sort_index()
    
    growth_rates = []
    for i in range(1, len(year_counts)):
        prev = year_counts.iloc[i-1]
        curr = year_counts.iloc[i]
        if prev > 0:
            rate = (curr - prev) / prev * 100
            growth_rates.append(rate)
    
    metrics['年度发文量'] = year_counts.to_dict()
    metrics['平均年增长率(%)'] = np.mean(growth_rates) if growth_rates else 0
    metrics['增长率标准差(%)'] = np.std(growth_rates) if growth_rates else 0

    # --- 2. 被引指标 ---
    citing_works = df['Citing Works Count'].dropna().astype(int)
    metrics['总被引次数'] = int(citing_works.sum())
    metrics['篇均被引'] = float(citing_works.mean())
    metrics['被引中位数'] = float(citing_works.median())
    metrics['高被引论文数(被引>50)'] = int((citing_works > 50).sum())
    metrics['零被引论文数'] = int((citing_works == 0).sum())

    # --- 3. h指数计算 ---
    sorted_citations = np.sort(citing_works)[::-1]
    h_index = sum(i + 1 <= sorted_citations[i] for i in range(len(sorted_citations)))
    metrics['h指数'] = h_index

    # --- 4. 来源期刊分析 ---
    journal_counts = df['Source Title'].value_counts().head(10)
    metrics['主要期刊分布'] = journal_counts.to_dict()

    # --- 5. 文献类型分布 ---
    type_counts = df['Publication Type'].value_counts()
    metrics['文献类型分布'] = type_counts.to_dict()

    # --- 6. 开放获取分析 ---
    open_access = df['Is Open Access'].dropna()
    metrics['开放获取比例(%)'] = float(open_access.mean() * 100)

    # --- 7. 作者分析 ---
    all_authors = []
    for authors in df['Author/s'].dropna().astype(str):
        all_authors.extend([a.strip() for a in authors.split(';')])
    author_counts = pd.Series(all_authors).value_counts().head(10)
    metrics['高产作者TOP10'] = author_counts.to_dict()
    metrics['作者总数'] = len(set(all_authors))
    metrics['篇均作者数'] = df['Author/s'].dropna().apply(lambda x: len([a.strip() for a in x.split(';')])).mean()

    # --- 8. 研究领域分布 ---
    fields = []
    for field in df['Fields of Study'].dropna().astype(str):
        fields.extend([f.strip() for f in field.split(';')])
    field_counts = pd.Series(fields).value_counts().head(15)
    metrics['研究领域分布TOP15'] = field_counts.to_dict()

    # --- 输出指标报告 ---
    output_file = os.path.join(output_dir, 'metrics_summary.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("            LLM多智能体领域文献计量指标分析报告\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("【一、时间维度指标】\n")
        f.write("-" * 40 + "\n")
        for year, count in metrics['年度发文量'].items():
            f.write(f"  {int(year)}年: {count}篇\n")
        f.write(f"\n  平均年增长率: {metrics['平均年增长率(%)']:.2f}%\n")
        f.write(f"  增长率标准差: {metrics['增长率标准差(%)']:.2f}%\n\n")

        f.write("【二、影响力指标】\n")
        f.write("-" * 40 + "\n")
        f.write(f"  总被引次数: {metrics['总被引次数']:,}\n")
        f.write(f"  篇均被引: {metrics['篇均被引']:.2f}\n")
        f.write(f"  被引中位数: {metrics['被引中位数']:.2f}\n")
        f.write(f"  高被引论文数(被引>50): {metrics['高被引论文数(被引>50)']}\n")
        f.write(f"  零被引论文数: {metrics['零被引论文数']}\n")
        f.write(f"  h指数: {metrics['h指数']}\n\n")

        f.write("【三、来源期刊TOP10】\n")
        f.write("-" * 40 + "\n")
        for journal, count in metrics['主要期刊分布'].items():
            f.write(f"  {journal}: {count}篇\n")
        f.write("\n")

        f.write("【四、文献类型分布】\n")
        f.write("-" * 40 + "\n")
        for doc_type, count in metrics['文献类型分布'].items():
            f.write(f"  {doc_type}: {count}篇 ({count/len(df)*100:.1f}%)\n")
        f.write("\n")

        f.write("【五、开放获取情况】\n")
        f.write("-" * 40 + "\n")
        f.write(f"  开放获取比例: {metrics['开放获取比例(%)']:.2f}%\n\n")

        f.write("【六、作者统计】\n")
        f.write("-" * 40 + "\n")
        f.write(f"  作者总数: {metrics['作者总数']:,}\n")
        f.write(f"  篇均作者数: {metrics['篇均作者数']:.2f}\n")
        f.write("\n  高产作者TOP10:\n")
        for author, count in metrics['高产作者TOP10'].items():
            f.write(f"    {author}: {count}篇\n")
        f.write("\n")

        f.write("【七、研究领域分布TOP15】\n")
        f.write("-" * 40 + "\n")
        for field, count in metrics['研究领域分布TOP15'].items():
            f.write(f"  {field}: {count}次\n")

    print(f"计量指标分析报告已保存至: {output_file}")
    return metrics


if __name__ == "__main__":
    calculate_metrics()