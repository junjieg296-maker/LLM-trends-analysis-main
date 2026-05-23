# 基于文献计量学的 LLM 多智能体协作前沿趋势追踪

![Status](https://img.shields.io/badge/Status-M3_Completed-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Data](https://img.shields.io/badge/Data-Lens.org-blueviolet?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-522_Papers-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

本仓库是《文献计量学、前沿趋势追踪与项目制学习框架》课程项目的最终提交版本。项目围绕 **大语言模型多智能体协作（LLM Multi-Agent Collaboration）** 领域，完成从检索式设计、数据清洗、计量指标计算、知识图谱可视化到 mini review 写作的完整可复现流程。

项目核心问题：

1. LLM 多智能体研究是否已经进入爆发期？
2. 该领域的核心主题、关键词结构和技术路线是什么？
3. 哪些作者、国家/地区和高被引论文正在推动该领域发展？
4. 当前研究有哪些值得进一步关注的空白？

## 核心结论

| 指标 | 结果 |
|---|---:|
| 原始记录 | 542 |
| 清洗后有效文献 | 522 |
| 时间范围 | 2020-2026 |
| 数据来源 | Lens.org Scholarly Works |
| 总被引次数 | 4,265 |
| h 指数 | 31 |
| 2025 年发文量 | 344 |
| 开放获取比例 | 73.18% |

主要发现：

- 领域在 2024-2025 年进入快速爆发期，2025 年发文量达到 344 篇。
- 高频主题集中在 `artificial intelligence`、`large language models`、`agentic ai`、`multi-agent systems`、`retrieval-augmented generation` 和 `ethics`。
- 作者合作网络仍较分散，说明该领域处于快速扩张期，尚未形成稳定核心作者群。
- 高被引 milestone 候选论文集中在 chemistry agents、robot planning、human-AI teaming、clinical agents 和 human-robot interaction 等方向。

## 最终图表

### 关键词共现图

![Keyword Co-occurrence Network](outputs/figures/keyword_cooccurrence_network.png)

### 作者合作网络

![Author Collaboration Network](outputs/figures/author_collaboration_network.png)

### 国家/地区分布

![Institution Country Distribution](outputs/figures/institution_country_network.png)

### Milestone 候选论文影响力图

![Milestone Paper Influence Map](outputs/figures/citation_network.png)

## 快速复现

```bash
pip install -r requirements.txt
python run_pipeline.py
```

重新生成提交级 M2 图表：

```bash
python src/polished_m2_figures.py
```

生成 Top 10 milestone 候选论文表：

```bash
python src/milestone_papers.py
```

## 仓库结构

```text
LLM-trends-analysis-main/
├── config/
│   └── query.yaml                         # 参数化检索式
├── data/
│   ├── README.md                          # 数据说明
│   ├── raw/lens-llm-agents-raw.csv        # Lens.org 原始导出数据
│   └── processed/cleaned_data.csv         # 清洗去重后的数据
├── docs/
│   └── graph_data_model.md                # 知识图谱数据模型
├── outputs/
│   ├── figures/                           # 项目图表
│   ├── metrics_summary.txt                # 计量指标汇总
│   ├── keyword_statistics.txt             # 关键词统计
│   ├── milestone_paper_candidates.md      # Top 10 milestone 候选论文
│   └── sensitivity_analysis_report.txt    # 参数敏感性分析
├── paper/
│   └── mini_review_final.md               # Mini review 终稿
├── reports/
│   ├── m1_data_quality_report.md          # M1 数据质量报告
│   ├── m2_metrics_analysis_report.md      # M2 计量分析报告
│   ├── m3_final_report.md                 # M3 终稿与可复现 Release 报告
│   ├── metrics_specification.md           # 指标规范
│   └── query_changelog.md                 # 检索式变更记录
├── src/
│   ├── data_quality.py                    # 数据清洗与质检
│   ├── metrics_analysis.py                # 计量指标计算
│   ├── keyword_cooccurrence.py            # 关键词共现
│   ├── network_analysis.py                # 合作/机构/引用网络
│   ├── sensitivity_analysis.py            # 参数敏感性分析
│   ├── milestone_papers.py                # Milestone 候选论文
│   └── polished_m2_figures.py             # 提交级图表生成
├── run_pipeline.py                        # 一键复现入口
├── requirements.txt                       # Python 依赖
├── RELEASE_NOTES.md                       # Release 说明
└── README.md
```

## 课程里程碑

| 阶段 | 目标 | 本仓库产出 |
|---|---|---|
| M1 | 数据与检索方案 | `config/query.yaml`, `reports/m1_data_quality_report.md`, `data/processed/cleaned_data.csv` |
| M2 | 计量分析与图谱产出 | `reports/m2_metrics_analysis_report.md`, `outputs/figures/`, `outputs/sensitivity_analysis_report.txt` |
| M3 | 终稿与可复现 Release | `paper/mini_review_final.md`, `reports/m3_final_report.md`, `run_pipeline.py`, `RELEASE_NOTES.md` |

## 团队分工

| 成员 | 角色 | 主要负责内容 |
|---|---|---|
| 高俊杰 | 组长 / 工程架构与代码统筹 | 仓库结构、流水线、复现命令、M3 整合 |
| 赵世铎 | 数据获取与检索策略 | Lens.org 检索、检索式参数化、数据导出 |
| 解明昊 | 数据清洗与质量控制 | 去重、字段完整度检查、数据质量报告 |
| 杨广宸 | 知识图谱与计量分析 | 关键词共现、合作网络、指标计算、图表 |
| 罗博伟 | 综述写作与查新整合 | Mini review、研究空白、结论整合 |

## 方法透明度

本项目完整记录以下信息：

- 数据库：Lens.org Scholarly Works
- 检索式：`config/query.yaml`
- 时间范围：2020-2026
- 文献类型：Article, Review, Conference Paper
- 清洗规则：DOI 与 Title 双重去重
- 依赖环境：`requirements.txt`
- 一键复现：`python run_pipeline.py`
- 参数敏感性：`outputs/sensitivity_analysis_report.txt`

## License

本项目采用 MIT License。
