# Release Notes

## v1.0-m3-final

本版本为课程项目 M3 最终提交版本，完成"终稿与可复现 Release"要求。

### 数据版本

- 数据来源：Lens.org Scholarly Works
- 原始记录数：542
- 清洗后有效记录数：522
- 时间范围：2020-2026
- 文献类型：Article, Review, Conference Paper
- 检索式配置：`config/query.yaml`
- 清洗后数据：`data/processed/cleaned_data.csv`

### 复现命令

```bash
pip install -r requirements.txt
python run_pipeline.py
```

单独重绘提交级图表：

```bash
python src/polished_m2_figures.py
```

### 本版本核心交付物

| 类型 | 文件 |
|---|---|
| M1 报告 | `reports/m1_data_quality_report.md` |
| M2 报告 | `reports/m2_metrics_analysis_report.md` |
| M3 报告 | `reports/m3_final_report.md` |
| Mini review 终稿 | `paper/mini_review_final.md` |
| 指标规范 | `reports/metrics_specification.md` |
| 检索式记录 | `config/query.yaml`, `reports/query_changelog.md` |
| 一键流水线 | `run_pipeline.py` |
| 提交级图表 | `outputs/figures/*.png` |
| Milestone 候选表 | `outputs/milestone_paper_candidates.md` |

### 功能性改动

1. 新增一键运行入口 `run_pipeline.py`。
2. 新增依赖文件 `requirements.txt`。
3. 新增 `src/milestone_papers.py` 输出 Top 10 高被引 milestone 候选论文。
4. 新增 `src/polished_m2_figures.py` 生成提交级 M2 图表。
5. 修复关键词共现中的重复关键词和自连边问题。
6. 修复作者统计中的 `null null` 等无效作者污染。
7. 移除词云脚本运行时下载停用词的网络依赖。

### 核心结果

- 2025 年发文量达到 344 篇，领域进入快速爆发期。
- 总被引次数为 4,265，h 指数为 31。
- 高频主题包括 LLMs、agentic AI、multi-agent systems、RAG、reinforcement learning、ethics。
- 作者合作网络显示领域仍处于分散扩张阶段。
- Top milestone 候选论文覆盖 chemistry agents、robot planning、clinical agents、human-AI teaming 等方向。
