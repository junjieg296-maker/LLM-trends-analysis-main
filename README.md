# 基于文献计量学的 LLM 多智能体协作研究趋势分析

![Status](https://img.shields.io/badge/Status-M3_Completed-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Data](https://img.shields.io/badge/Data_Source-Lens.org-blueviolet?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-522_Papers-orange?style=flat-square)
![Method](https://img.shields.io/badge/Method-Bibliometrics_+_Knowledge_Graph-teal?style=flat-square)

本项目是《文献计量学、前沿趋势追踪与项目制学习框架》课程的 GitHub 项目成果，主题为 **大语言模型多智能体协作研究的文献计量分析与综述写作**。

项目围绕 LLM multi-agent collaboration 这一快速发展的交叉研究方向，基于 Lens.org Scholarly Works 构建 2020-2026 年文献数据集，并完成从检索式设计、数据清洗、质量评估、计量指标计算、知识图谱构建、参数敏感性分析，到 mini review 写作与答辩 PPT 归档的完整流程。

本仓库的核心目标不是只展示几张图，而是形成一条可复现、可解释、可答辩的证据链：

```text
Lens.org 检索
  -> 原始数据导出
  -> DOI / Title 去重
  -> 字段质量评估
  -> 计量指标分析
  -> 关键词 / 作者 / 引用 / 共被引图谱
  -> milestone 论文识别
  -> mini review 综述写作
  -> GitHub 项目归档与答辩展示
```

---

## 项目研究问题

本项目试图回答以下四个问题：

| 编号 | 研究问题 | 对应产出 |
|---|---|---|
| RQ1 | LLM 多智能体协作研究在 2020-2026 年经历了怎样的发展阶段？ | 年度发文趋势、增长率、影响力指标 |
| RQ2 | 当前研究主题主要集中在哪些关键词、技术层次和应用场景？ | 关键词共现网络、主题架构图 |
| RQ3 | 高被引论文和共被引关系能否支撑综述中的技术叙事线？ | milestone 候选论文、引用网络、共被引网络 |
| RQ4 | 如何把文献计量图谱转化为课程项目可提交的 mini review？ | `paper/mini_review_final.md`、M3 release 报告、答辩 PPT |

---

## 团队成员与任务分工

本项目采用“数据获取 - 数据清洗 - 计量分析 - 图谱构建 - 综述写作 - 工程归档”的流水线式分工。每位成员的工作都绑定到具体目录、脚本、报告或图表，便于在 GitHub 中追踪贡献。

| 成员 | 项目角色 | 主要负责内容 | 对应交付物 |
|---|---|---|---|
| 高俊杰 | 组长 / 工程架构与代码统筹 | 负责项目整体结构设计、代码组织、自动化运行入口、README 与最终归档；统筹 M1-M3 成果整合，保证项目能够以 GitHub 形式提交和复现。 | `run_pipeline.py`、`requirements.txt`、`README.md`、`RELEASE_NOTES.md`、项目目录整理 |
| 赵世铎 | 数据获取与检索策略规划 | 负责 Lens.org 检索策略设计，围绕 `(Object) AND (Method)` 逻辑确定关键词组合、时间范围、文献类型和语言限制；记录检索口径与策略变化。 | `config/query.yaml`、`data/raw/lens-llm-agents-raw.csv`、`reports/query_changelog.md`、`CHANGELOG.md` |
| 解明昊 | 数据清洗与质量控制 | 负责原始数据去重、字段标准化、缺失值检查和质量评估；基于 DOI 与 Title 双重去重，将 542 条原始记录清洗为 522 篇有效文献。 | `data/processed/cleaned_data.csv`、`src/data_quality.py`、`reports/m1_data_quality_report.md` |
| 杨广宸 | 计量分析与知识图谱构建 | 负责年度趋势、关键词共现、作者合作、机构/国家分布、引用网络、共被引网络和参数敏感性分析；输出 M2 阶段核心图表和指标结果。 | `src/metrics_analysis.py`、`src/keyword_cooccurrence.py`、`src/network_analysis.py`、`src/sensitivity_analysis.py`、`outputs/figures/`、`outputs/sensitivity_analysis_report.txt` |
| 罗博伟 | 文献筛选与综述写作 | 负责将 M1-M2 的计量证据转化为综述结构，整理 milestone 候选论文、主题叙事线、挑战与未来方向；参与 mini review 终稿和答辩材料组织。 | `outputs/milestone_paper_candidates.md`、`paper/mini_review_final.md`、`reports/m3_final_report.md`、`outputs/review_figures/` |

### 分工逻辑

| 阶段 | 小组协作重点 | 主要负责人 |
|---|---|---|
| M1 数据与检索方案 | 检索式设计、原始数据导出、去重清洗、字段质量评估 | 赵世铎、解明昊、高俊杰 |
| M2 计量分析与图谱 | 指标计算、关键词共现、作者合作、机构分布、引用与共被引网络、敏感性分析 | 杨广宸、高俊杰 |
| M3 综述与项目归档 | milestone 论文识别、mini review 写作、图文解释、release 报告、答辩 PPT | 罗博伟、高俊杰、全组协作 |

---

## 数据来源与检索策略

### 数据来源

| 项目 | 内容 |
|---|---|
| 数据库 | Lens.org Scholarly Works |
| 时间范围 | 2020-2026 |
| 文献类型 | Article, Review, Conference Paper / Conference Proceedings Article |
| 语言 | English |
| 原始记录数 | 542 条 |
| 清洗后有效文献 | 522 篇 |
| 去重方法 | DOI 去重 + Title 去重 |
| 核心数据文件 | `data/processed/cleaned_data.csv` |

> 说明：2026 年数据为采集时点数据，年份尚未结束，因此在趋势分析中只作为阶段性观察，不与完整年份直接比较。

### 检索式设计

本项目采用 `(Object) AND (Method)` 的布尔检索逻辑，避免样本过宽或主题跑偏。

| 检索模块 | 关键词组 | 作用 |
|---|---|---|
| Object | `Large Language Model*`, `LLM*`, `Generative AI`, `Foundation Model*`, `ChatGPT` | 锁定大语言模型和生成式 AI 研究对象 |
| Method | `Multi-agent*`, `Collaboration`, `Coordination`, `Cooperation`, `Multi-agent system*` | 锁定多智能体、协作、协调和合作机制 |

检索策略配置与版本记录见：

- `config/query.yaml`
- `reports/query_changelog.md`
- `CHANGELOG.md`

---

## 数据筛选与质量控制

本项目采用 PRISMA 式筛选思路组织数据清洗流程：

| 阶段 | 操作 | 数量 |
|---|---|---:|
| Identification | Lens.org 初始检索导出 | 542 |
| Deduplication | 基于 DOI 与 Title 双重去重 | -20 |
| Included | 纳入后续计量分析的有效样本 | 522 |

核心字段覆盖率如下：

| 字段 | 覆盖率 | 对后续分析的意义 |
|---|---:|---|
| Title | 100.00% | 支持标题词频、关键词识别和主题分析 |
| Year | 100.00% | 支持年度发文趋势与阶段判断 |
| Abstract | 98.28% | 支持后续语义扩展和主题解释 |
| References | 81.99% | 支持引用网络和文献共被引分析 |
| DOI | 99.81% | 支持去重、溯源和候选 milestone 识别 |

完整质量评估见：

- `reports/m1_data_quality_report.md`
- `src/data_quality.py`

---

## 方法框架

本项目采用“定量指标 + 知识图谱 + 综述解释”的组合方法。

| 分析维度 | 方法 / 工具 | 主要输出 |
|---|---|---|
| 数据清洗 | Python, Pandas | 去重后的 522 篇有效文献 |
| 年度趋势 | 描述性统计, Matplotlib | 2020-2026 年发文增长趋势 |
| 影响力指标 | 被引次数、篇均被引、h 指数 | 领域关注度和高影响论文识别 |
| 关键词共现 | NetworkX 共现网络 | 研究主题与技术层次 |
| 作者合作 | 社会网络分析 | 合作结构、核心团队和分散程度 |
| 机构 / 国家分布 | 元数据统计与网络可视化 | 研究力量空间分布 |
| 引用网络 | 有向引用关系 | 高影响论文及知识传播路径 |
| 文献共被引 | Co-citation network | 知识基础和主题簇识别 |
| 参数敏感性 | 阈值扫描、时间窗口比较 | 验证结果稳健性 |
| 综述写作 | 计量证据转技术叙事 | `paper/mini_review_final.md` |

综述方法流程图：

![Literature retrieval and review design](outputs/review_figures/fig1_methodology_workflow.png)

---

## 核心结果概览

### 1. 年度发文趋势：2024-2025 年进入爆发期

| 年份 | 发文量 | 同比增长率 |
|---:|---:|---:|
| 2020 | 1 | - |
| 2021 | 2 | +100% |
| 2022 | 6 | +200% |
| 2023 | 19 | +217% |
| 2024 | 81 | +326% |
| 2025 | 344 | +325% |
| 2026 | 69 | 数据未完整 |

关键判断：

- 2020-2023 年处于早期探索阶段。
- 2024 年开始加速，2025 年进入爆发式增长阶段。
- 2026 年为采集时点数据，不与完整年份直接比较。

![Publication growth and development stages](outputs/review_figures/fig2_publication_growth_stages.png)

### 2. 影响力指标：高热度与新论文稀释并存

| 指标 | 数值 | 解释 |
|---|---:|---|
| 总被引次数 | 4,265 | 领域整体学术关注度较高 |
| 篇均被引 | 8.17 | 体现已有研究影响力 |
| 被引中位数 | 1.00 | 受大量新近论文影响 |
| 高被引论文数 | 20 | 被引次数 > 50 的 milestone 候选基础 |
| 零被引论文数 | 236 | 约 45.2%，主要来自新近发表文献 |
| h 指数 | 31 | 说明已有较稳定的高影响论文基础 |

### 3. 研究主题：形成四层主题结构

关键词共现结果显示，LLM 多智能体协作研究主要形成四个层次：

| 层次 | 代表关键词 | 含义 |
|---|---|---|
| 技术底座 | `large language models`, `artificial intelligence`, `machine learning`, `NLP` | 多智能体系统能力依赖 LLM 和 AI 基础能力 |
| 协作架构 | `agentic ai`, `multi-agent systems`, `ai agents` | 研究重点从单模型输出转向角色分工和任务协作 |
| 能力增强 | `retrieval-augmented generation`, `reinforcement learning`, `planning` | 关注知识更新、工具调用、反馈学习与复杂规划 |
| 治理应用 | `ethics`, `human-robot interaction`, `digital health`, `robot` | 多智能体系统进入高约束应用与安全治理场景 |

![Thematic architecture of LLM multi-agent collaboration](outputs/review_figures/fig3_thematic_architecture.png)

### 4. 研究力量：开放、分散、跨学科

| 指标 | 数值 |
|---|---:|
| 期刊论文 | 383 篇，占 73.4% |
| 会议论文 | 139 篇，占 26.6% |
| 开放获取比例 | 73.18% |
| 作者总数 | 2,564 / 2,565 左右，受清洗口径影响 |
| 篇均作者数 | 约 5.07-5.10 |
| 作者合作网络过滤后规模 | 51 个节点，48 条边 |

解释：

- 该领域知识传播壁垒较低，开放获取比例较高。
- 高产作者最高发文量仅 3 篇，说明核心作者群体尚未高度集中。
- 作者合作网络在过滤一次性合作后明显收缩，表明稳定合作团队仍较分散。
- 来源覆盖 AAMAS、Frontiers in Robotics and AI、Frontiers in Artificial Intelligence、Scientific Reports、Sensors、NPJ Digital Medicine 等，体现 AI、机器人、人机交互、医学与工程系统的交叉特征。

### 5. 高被引论文与知识基础

本项目基于 Lens.org 被引次数输出 Top 10 milestone 候选论文，并结合主题内容归纳综述技术主线。

![Milestone candidate matrix](outputs/review_figures/fig4_milestone_roadmap.png)

同时，项目新增文献共被引网络，用于解释高影响论文背后的知识基础和主题簇：

![Reference co-citation network](outputs/review_figures/fig6_reference_cocitation_network.png)

解释方式：

- 高被引图回答“哪些论文重要”。
- 共被引网络回答“这些重要论文背后共同依赖哪些知识基础”。
- 两者结合可以避免综述只罗列论文，而能形成技术叙事线。

---

## M1-M3 阶段成果

### M1：数据采集、清洗与质量评估

M1 阶段完成了文献数据集构建和基础质量控制。

主要成果：

- 设计 Lens.org 检索策略与配置文件。
- 导出 542 条原始记录。
- 基于 DOI 与 Title 去重，得到 522 篇有效文献。
- 统计 Title、Year、Abstract、References、DOI 等字段覆盖率。
- 输出 M1 数据质量报告。
- 生成年度趋势图和标题词云，形成初步主题判断。

相关文件：

- `config/query.yaml`
- `data/raw/lens-llm-agents-raw.csv`
- `data/processed/cleaned_data.csv`
- `src/data_quality.py`
- `src/trend_analysis.py`
- `src/word_cloud_analysis.py`
- `reports/m1_data_quality_report.md`
- `outputs/figures/publication_trend.png`
- `outputs/figures/wordcloud_titles.png`

### M2：计量分析与知识图谱构建

M2 阶段完成系统的文献计量指标分析和图谱可视化。

主要成果：

- 计算年度发文量、平均年增长率、被引次数、篇均被引、h 指数等指标。
- 构建关键词共现网络，识别研究主题结构。
- 构建作者合作网络，分析团队合作分散程度。
- 构建机构 / 国家分布图，观察研究力量空间分布。
- 构建引用网络和共被引网络，支撑 milestone 论文与知识基础分析。
- 完成关键词阈值、作者合作阈值、时间窗口等参数敏感性测试。

相关文件：

- `src/metrics_analysis.py`
- `src/keyword_cooccurrence.py`
- `src/network_analysis.py`
- `src/sensitivity_analysis.py`
- `src/milestone_papers.py`
- `reports/m2_metrics_analysis_report.md`
- `reports/metrics_specification.md`
- `outputs/metrics_summary.txt`
- `outputs/keyword_statistics.txt`
- `outputs/milestone_paper_candidates.md`
- `outputs/sensitivity_analysis_report.txt`
- `outputs/figures/keyword_cooccurrence_network.png`
- `outputs/figures/author_collaboration_network.png`
- `outputs/figures/institution_country_network.png`
- `outputs/figures/citation_network.png`
- `outputs/figures/reference_cocitation_network.png`

### M3：Mini Review、证据整合与项目归档

M3 阶段将 M1-M2 的计量证据转化为可提交的综述文章和 GitHub release 版本。

主要成果：

- 完成 mini review 终稿。
- 将关键词图谱、高被引论文和共被引网络转化为综述中的技术叙事线。
- 归纳四条主要技术主线：
  - 多智能体任务规划与自动化工作流
  - 科学发现与自驱动实验室
  - 人机协作与人类监督
  - 医疗、机器人等垂直行业智能体
- 总结未来挑战：
  - 评价体系不统一
  - 协作机制可解释性不足
  - 垂直场景验证有限
  - 安全治理和责任分配复杂化
- 完成 M3 release 报告、答辩 PPT 和最终项目归档。

相关文件：

- `paper/mini_review_final.md`
- `reports/m3_final_report.md`
- `RELEASE_NOTES.md`
- `outputs/review_figures/fig1_methodology_workflow.png`
- `outputs/review_figures/fig2_publication_growth_stages.png`
- `outputs/review_figures/fig3_thematic_architecture.png`
- `outputs/review_figures/fig4_milestone_roadmap.png`
- `outputs/review_figures/fig5_challenges_agenda.png`
- `outputs/review_figures/fig6_reference_cocitation_network.png`

---

## 图表索引

### M2 计量分析图表

| 图表 | 文件路径 | 用途 |
|---|---|---|
| 年度发文趋势图 | `outputs/figures/publication_trend.png` | 展示 2020-2026 年发文增长 |
| 标题词云 | `outputs/figures/wordcloud_titles.png` | 初步识别标题高频主题 |
| 关键词共现网络 | `outputs/figures/keyword_cooccurrence_network.png` | 识别主题关联与技术层次 |
| 作者合作网络 | `outputs/figures/author_collaboration_network.png` | 分析研究团队合作结构 |
| 机构 / 国家分布网络 | `outputs/figures/institution_country_network.png` | 展示研究力量空间分布 |
| 引用网络 / 高影响图谱 | `outputs/figures/citation_network.png` | 识别高影响论文与知识传播路径 |
| 文献共被引网络 | `outputs/figures/reference_cocitation_network.png` | 识别共同知识基础和主题簇 |

### 综述与答辩图表

| 图表 | 文件路径 | 用途 |
|---|---|---|
| 文献检索与综述设计流程 | `outputs/review_figures/fig1_methodology_workflow.png` | 说明从数据到综述的研究流程 |
| 年度发文阶段图 | `outputs/review_figures/fig2_publication_growth_stages.png` | 支撑“2024-2025 爆发期”判断 |
| 主题架构图 | `outputs/review_figures/fig3_thematic_architecture.png` | 将关键词共现转化为四层主题框架 |
| Milestone 候选矩阵 | `outputs/review_figures/fig4_milestone_roadmap.png` | 将高被引论文转化为技术叙事线 |
| 挑战与未来议程 | `outputs/review_figures/fig5_challenges_agenda.png` | 总结评价、解释性、场景验证和安全治理问题 |
| 文献共被引网络 | `outputs/review_figures/fig6_reference_cocitation_network.png` | 补充 milestone 背后的知识基础 |

---

## 快速复现

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 一键运行完整流水线

```bash
python run_pipeline.py
```

该命令用于串联数据清洗、指标计算、图谱生成和敏感性分析等核心步骤。

### 3. 单独运行常用脚本

```bash
# 数据质量评估
python src/data_quality.py

# 年度趋势分析
python src/trend_analysis.py

# 计量指标分析
python src/metrics_analysis.py

# 关键词共现网络
python src/keyword_cooccurrence.py

# 作者、机构、引用和共被引网络
python src/network_analysis.py

# 参数敏感性分析
python src/sensitivity_analysis.py

# 生成提交级 M2 图表
python src/polished_m2_figures.py

# 生成综述图表
python src/paper_review_figures.py
```

---

## 项目目录结构

```text
LLM-trends-analysis-main/
├── config/
│   └── query.yaml                         # Lens.org 检索策略配置
├── data/
│   ├── raw/
│   │   └── lens-llm-agents-raw.csv         # 原始导出数据
│   └── processed/
│       └── cleaned_data.csv                # 清洗去重后的有效数据集
├── docs/
│   └── graph_data_model.md                 # 知识图谱数据模型说明
├── outputs/
│   ├── figures/                            # M2 计量分析图表
│   ├── review_figures/                     # 综述和答辩图表
│   ├── metrics_summary.txt                 # 指标汇总
│   ├── keyword_statistics.txt              # 关键词统计
│   ├── milestone_paper_candidates.md       # Top 10 milestone 候选论文
│   └── sensitivity_analysis_report.txt     # 参数敏感性分析
├── paper/
│   └── mini_review_final.md                # 综述终稿
├── reports/
│   ├── m1_data_quality_report.md           # M1 数据质量报告
│   ├── m2_metrics_analysis_report.md       # M2 计量分析报告
│   ├── m3_final_report.md                  # M3 release 报告
│   └── metrics_specification.md            # 指标规范说明
├── src/
│   ├── data_quality.py
│   ├── trend_analysis.py
│   ├── word_cloud_analysis.py
│   ├── metrics_analysis.py
│   ├── keyword_cooccurrence.py
│   ├── network_analysis.py
│   ├── sensitivity_analysis.py
│   ├── milestone_papers.py
│   ├── polished_m2_figures.py
│   └── paper_review_figures.py
├── run_pipeline.py                         # 一键复现入口
├── requirements.txt                        # Python 依赖
├── RELEASE_NOTES.md
└── README.md
```

---

## 主要结论

1. **LLM 多智能体协作研究已经进入高速增长期。** 2024-2025 年发文量快速跃升，2025 年达到 344 篇，说明该领域已从早期探索进入高强度扩张阶段。

2. **研究主题不是单一模型能力问题，而是系统协作问题。** 关键词结构显示，该领域从 LLM/AI 技术底座延伸到智能体协作架构、RAG/RL 能力增强以及治理与垂直应用。

3. **研究力量仍较分散，尚未形成高度集中的核心作者群体。** 高产作者最高发文量仅为 3 篇，作者合作网络过滤后规模明显收缩，说明领域仍处于快速扩张和范式重组阶段。

4. **高被引论文和共被引网络可以支撑综述结构。** milestone 候选矩阵帮助识别代表性论文，共被引网络进一步揭示共同知识基础，使综述不只是罗列论文，而能形成技术叙事线。

5. **未来研究需要从演示型 agent 走向可评价、可解释、可审计的智能体协作系统。** 评价基准、协作日志、证据链、人类监督和安全治理将是后续关键方向。

---

## 局限性说明

本项目仍存在以下边界：

- 2026 年数据尚未完整，因此趋势解释中不能把 2026 与完整年份直接比较。
- References 字段覆盖率为 81.99%，足以开展初步引用与共被引分析，但仍可能受到字段缺失影响。
- Lens.org 元数据中的国家、机构和作者字段可能存在缺失或格式差异。
- 高被引 milestone 候选论文主要基于 Lens.org 被引次数排序，后续可进一步结合 burst detection、centrality、cluster position 等指标增强判断。
- 当前图谱以课程项目可复现为优先目标，后续可以继续接入 VOSviewer / CiteSpace 进行更严格的科学知识图谱分析。

---

## 课程交付物

| 类型 | 文件 |
|---|---|
| M1 数据质量报告 | `reports/m1_data_quality_report.md` |
| M2 计量分析报告 | `reports/m2_metrics_analysis_report.md` |
| M3 release 报告 | `reports/m3_final_report.md` |
| Mini review 终稿 | `paper/mini_review_final.md` |
| 指标规范 | `reports/metrics_specification.md` |
| 关键图表 | `outputs/figures/`, `outputs/review_figures/` |
| 一键复现入口 | `run_pipeline.py` |
| 答辩 PPT | 已生成并另存为 `LLM_multi_agent_week13_defense_expanded.pptx` |

---

## 许可

本项目采用 MIT License，详见 `LICENSE`。
