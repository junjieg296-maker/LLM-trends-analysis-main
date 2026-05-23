# M3 终稿与可复现 Release 报告

## 1. 项目概况

本项目围绕"大语言模型多智能体协作（LLM Multi-Agent Collaboration）"开展文献计量学分析与前沿趋势追踪。项目基于 Lens.org Scholarly Works 数据，构建了 2020-2026 年 LLM 多智能体相关研究文献数据集，并完成检索式参数化、数据清洗、计量指标计算、知识图谱可视化、参数敏感性分析和 mini review 终稿写作。

项目采用课程要求的"项目制、可复现"框架组织。仓库保留完整的数据链、代码链、图表链和报告链，支持通过一键命令复现核心输出。

## 2. M1-M3 交付物完成情况

| 阶段 | 课程目标 | 本项目交付物 | 完成情况 |
|---|---|---|---|
| M1 | 数据与检索方案 | `config/query.yaml`, `reports/query_changelog.md`, `src/data_quality.py`, `reports/m1_data_quality_report.md` | 完成 |
| M2 | 计量分析产出 | `reports/m2_metrics_analysis_report.md`, `reports/metrics_specification.md`, `outputs/figures/`, `outputs/sensitivity_analysis_report.txt` | 完成 |
| M3 | 终稿与可复现 Release | `paper/mini_review_final.md`, `reports/m3_final_report.md`, `RELEASE_NOTES.md`, `run_pipeline.py`, `requirements.txt` | 完成 |

## 3. 数据与检索口径

本项目数据来源为 Lens.org Scholarly Works。检索策略采用 `(Object) AND (Method)` 的布尔逻辑：

- Object 词组：`Large Language Model*`, `LLM*`, `Generative AI`, `Foundation Model*`, `ChatGPT`
- Method 词组：`Multi-agent*`, `Collaboration`, `Coordination`, `Cooperation`, `Multi-agent system*`
- 时间范围：2020-2026
- 文献类型：Article, Review, Conference Paper
- 语言：English

原始数据共 542 条记录。经 DOI 与 Title 双重去重后，得到 522 条有效记录。核心字段质量如下：

| 字段 | 缺失率 | 说明 |
|---|---:|---|
| Title | 0.00% | 支持标题词频与主题识别 |
| Author/s | 0.38% | 支持作者合作网络 |
| Abstract | 1.72% | 支持后续语义分析扩展 |
| References | 18.01% | 支持引用网络的初步构建 |
| DOI | 0.19% | 支持去重与溯源 |

## 4. 可复现运行方式

项目根目录提供 `requirements.txt` 与 `run_pipeline.py`。标准复现流程如下：

```bash
pip install -r requirements.txt
python run_pipeline.py
```

若只需要重新生成提交用的 M2 美化图，可运行：

```bash
python src/polished_m2_figures.py
```

主要输出目录如下：

| 目录/文件 | 内容 |
|---|---|
| `data/raw/` | Lens.org 原始导出数据 |
| `data/processed/cleaned_data.csv` | 清洗去重后的有效数据 |
| `outputs/figures/` | 发文趋势、词云、关键词共现、作者合作、国家分布、里程碑论文图 |
| `outputs/metrics_summary.txt` | 文献计量指标汇总 |
| `outputs/keyword_statistics.txt` | 高频关键词与共现关系 |
| `outputs/milestone_paper_candidates.md` | Top 10 里程碑候选论文 |
| `outputs/sensitivity_analysis_report.txt` | 参数敏感性分析 |
| `reports/` | M1、M2、M3 阶段报告与方法规范 |
| `paper/mini_review_final.md` | Mini review 终稿 |

## 5. 功能性改动与工程化完善

本项目完成了可验收的功能性改动与工程化整理：

1. 新增 `run_pipeline.py`，将原本分散的清洗、统计、图谱和敏感性分析脚本整合为一键运行流水线。
2. 新增 `requirements.txt`，固定项目核心依赖，满足课程对可复现环境的要求。
3. 修复关键词共现统计逻辑，在单篇文献内先对关键词进行标准化和去重，避免出现自连边。
4. 修复作者统计与作者合作网络中的空值污染，过滤 `null`、`null null`、`nan`、`unknown` 等无效作者名。
5. 新增 `src/milestone_papers.py`，输出 Top 10 高被引 milestone 候选论文表。
6. 新增 `src/polished_m2_figures.py`，生成提交级 M2 图表，提升 GitHub 展示和答辩可读性。
7. 移除词云脚本中的运行时下载逻辑，降低复现时的网络依赖风险。

## 6. M2 核心结果汇总

### 6.1 发文趋势

2020-2026 年有效样本共 522 篇。年度发文量从 2020 年的 1 篇增长到 2025 年的 344 篇，显示该领域在 2024-2025 年进入快速爆发期。2026 年已有 69 篇，但由于年份尚未结束，不直接与完整年份比较。

### 6.2 影响力指标

| 指标 | 数值 |
|---|---:|
| 总被引次数 | 4,265 |
| 篇均被引 | 8.17 |
| 被引中位数 | 1.00 |
| 高被引论文数（>50） | 20 |
| 零被引论文数 | 236 |
| h 指数 | 31 |

该结果说明领域整体关注度较高，但大量 2024-2025 年新论文仍处于引用累积早期。

### 6.3 关键词主题结构

关键词共现结果显示，研究主题集中在四个层次：

1. 技术底座：artificial intelligence, large language models, machine learning, NLP
2. 智能体架构：agentic AI, multi-agent systems, AI agents
3. 能力增强：retrieval-augmented generation, reinforcement learning, planning
4. 治理与应用：ethics, human-robot interaction, digital health

### 6.4 作者与机构分布

作者合作网络显示该领域研究团队仍较分散。过滤一次性合作后，重复合作组件规模较小，尚未形成稳定的跨团队核心枢纽。国家/地区分布显示，瑞士、美国、英国等是 Lens.org 元数据中出现频次较高的来源国家，同时也存在部分国家字段缺失。

### 6.5 Milestone 候选论文

项目基于 Lens.org 被引次数输出 Top 10 milestone 候选论文，作为第一轮知识锚点识别。该表已保存至 `outputs/milestone_paper_candidates.md`，并在 `outputs/figures/citation_network.png` 中以更适合展示的图形方式呈现。

## 7. 参数与质量控制

项目记录了关键词共现阈值、作者合作阈值、时间窗口和节点度过滤等敏感性测试。结果显示：

- 关键词共现阈值为 2 时，能够在保留信息量和过滤噪声之间取得较好平衡。
- 作者合作阈值从 1 提升到 2 后，网络快速收缩，说明领域合作关系仍以一次性合作为主。
- 全时间窗口 2020-2026 的 h 指数为 31，与 2022-2025 窗口结果一致，影响力判断较稳定。

## 8. 结论

本项目已完成课程 M3 阶段要求，形成了可提交的 GitHub 项目版本。项目不仅包含数据、代码、图表和报告，还提供了可复现命令与终稿 mini review。计量结果表明，LLM 多智能体协作研究处于高速成长期，研究主题从 LLM 基础能力扩展到智能体协作架构、RAG/RL 能力增强、机器人/医疗等垂直应用以及伦理治理议题。该领域仍具有团队分散、评价标准不统一、垂直场景验证不足等特点，适合作为后续研究和课程答辩的前沿主题。
