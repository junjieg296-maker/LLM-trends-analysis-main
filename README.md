# 🚀 基于文献计量学的大语言模型多智能体协作 (LLM Multi-Agent) 前沿趋势追踪

![Status](https://img.shields.io/badge/Status-M1_Completed-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Data](https://img.shields.io/badge/Data_Source-Lens.org-blueviolet?style=flat-square)

本项目为《文献计量学、前沿趋势追踪与项目制学习框架》课程的阶段性开源产出。

本项目严格落实“项目制·可复现”的核心学术要求，绝不使用“随便试出来”的参数或黑盒操作。我们旨在通过对**大语言模型多智能体协作 (LLM Multi-Agent Collaboration)** 领域的学术文献进行系统性的检索、清洗、计量分析与图谱可视化。项目尤其关注 **LLM 智能体在垂直硬核领域的交叉应用（如硬件 EDA、RTL/Verilog 代码生成与系统测试）**，旨在精准刻画该技术从“通用文本生成”向“复杂工程协作”演化的脉络，并发掘未来高价值的研究空白。

---

## 🛠️ 核心技术栈与工具链 (Tech Stack)

* **数据来源**：[Lens.org](https://www.lens.org/) (保障全字段覆盖率与高信度学术源)
* **数据清洗与分析**：`Python 3.11`, `Pandas` (提供高效的向量化去重与缺失值处理)
* **可视化引擎**：`Matplotlib` (时序分析), `WordCloud` (语义分析)
* **知识图谱 (M2规划)**：`NetworkX`, `VOSviewer` (网络拓扑构建与共现图谱渲染)
* **工程协同**：`Git` & `GitHub Desktop` (全流程版本控制)

---

## 👥 团队成员与精细化分工

为确保分析全流程的可追溯性，团队 5 名成员按照文献计量的标准流水线进行了严格的职责划分与交付物绑定：

| 姓名 | 角色 | 核心工作内容与具体交付物细则 (M1-M3 全周期) | 负责目录 |
| :--- | :--- | :--- | :--- |
| **[高俊杰]** | **组长 / 工程架构与代码统筹** | **构建项目自动化底座。**<br>1. **环境配置**：管理 `requirements.txt`，确保跨设备 Python 环境一致性。<br>2. **版本控制**：制定 Git 提交规范（Conventional Commits），严格执行 `data/raw` 原始数据不上云的隐私红线。<br>3. **流水线开发**：主导 `src/` 下核心 Python 脚本编写，将零散清洗逻辑封装为可一键运行的自动化数据处理 Pipeline (流水线)。 | `src/`<br>根目录配置 |
| **[赵世铎]** | **数据获取与检索策略规划** | **负责检索逻辑的参数化与查全/查准平衡。**<br>1. **策略迭代**：在 `config/query.yaml` 中利用 `(Object) AND (Method)` 布尔逻辑执行多次检索调优，并扩展核心同义词。<br>2. **精准导出**：在 Lens.org 严格限定时间范围（2020-2026）与文献类型（Article/Review），无损导出包含摘要与引文的 542 篇初始 CSV 数据。<br>3. **追踪日志**：主笔 `CHANGELOG.md` 中的检索策略版本更迭记录。 | `config/`<br>`data/raw/` |
| **[解明昊]** | **数据清洗与质量风控 (QA)** | **负责消除脏数据，保障底层数据源的极高纯净度。**<br>1. **精准去重**：利用 Pandas 编写基于 DOI 和 Title 的双重校验去重脚本，成功拦截并剔除冗余文献。<br>2. **清洗填补**：处理摘要和引文中的缺失字段（NaN），清洗格式错乱，输出 522 篇标准化的 `processed` 数据集。<br>3. **质检报告**：输出包含各项核心字段（Title/Abstract/Year）覆盖率的自动化自检表格。 | `data/processed/`<br>`reports/` |
| **[杨广宸]** | **知识图谱构建与计量算法** | **负责科学地图渲染与量化特征挖掘。**<br>1. **时序语义分析 (M1)**：利用 Matplotlib/WordCloud 输出领域发文趋势（指数级爆发）与标题高频词核心画像。<br>2. **图谱算法设计 (M2)**：基于 NetworkX 设计节点权重与连边逻辑，筹备社区发现聚类算法。<br>3. **可视化渲染**：利用 VOSviewer 产出高颜值的科学共被引网络与关键词共现图谱。 | `outputs/`<br>`docs/` |
| **[罗博伟]** | **文献筛选与查新学术写作** | **负责把控综述学术深度与 PRISMA 规范表达。**<br>1. **筛选漏斗**：严格执行 PRISMA 2020 标准，为剔除样本编制 Reason Code 排查记录表。<br>2. **交叉应用挖掘**：从宏观词云趋势中敏锐提取“LLM 在硬件 EDA 与 RTL 代码生成”等前沿且硬核的交叉研究空白点。<br>3. **定稿整合**：利用 Zotero/EndNote 等工具管理引文，整合量化图表，主笔最终 6-8 页的高水平综述手稿。 | `reports/`<br>`paper/` |

---

## 📁 规范化目录结构 (Directory Structure)

项目确立了单一事实来源 (Single Source of Truth)，严禁数据与代码逻辑混用：

```text
LLM-trends-analysis-main/
├── config/              # 检索策略层：参数化配置文件 query.yaml (v0.1)
├── data/                
│   ├── raw/             # (受 .gitignore 保护) Lens.org 导出的 542 篇原始 CSV
│   └── processed/       # 清洗去重后的 522 篇高纯度数据集 (计量唯一数据源)
├── outputs/figures/     # 表现层：存放趋势图、词云等可视化图片
├── reports/             # 控制层：PRISMA 流程与 data_quality.md 质检报告
├── src/                 # 逻辑层：自动化清洗、去重与图表生成脚本
├── paper/               # 输出层：学术综述稿件初稿与定稿
├── docs/                # 定义层：知识图谱数据模型设计草图
├── CHANGELOG.md         # 项目核心里程碑与检索策略版本更迭记录
└── requirements.txt     # Python 依赖清单
```

---

## 🚀 快速复现指南 (Quick Start)

本项目秉持“完全开源、一键复现”原则，任何研究人员均可通过以下步骤复现本项目的 M1 数据清洗与可视化分析结果：

```bash
# 1. 克隆本仓库到本地
git clone [https://github.com/junjieg296-maker/LLM-trends-analysis-main.git](https://github.com/junjieg296-maker/LLM-trends-analysis-main.git)
cd LLM-trends-analysis-main

# 2. 安装 Python 依赖环境
pip install -r requirements.txt

# 3. 运行自动化质检与可视化流水线
python src/data_quality.py
```
> **注**：运行成功后，最新的趋势图与词云将自动生成并保存在 `outputs/figures/` 目录下，控制台将输出字段缺失率验证报告。

---

## 📅 项目核心里程碑 (Milestones)

### [x] M1 阶段：数据与检索方案验证（第 4 周）
* 确立了 v0.1 版 YAML 检索配置，完成数据采集。
* 输出 `data_quality.md` 报告，确立 PRISMA 筛选流程。
* 生成发文趋势图与词云，初步形成领域前沿洞察。

### [ ] M2 阶段：计量分析与图谱产出（第 10 周）
* 设计严密的图数据模型草图（定义节点、连边及权重）。
* 构建作者共现网络、机构合作网络及高频关键词共现图谱。
* 编写包含计算公式及参数敏感性测试的计量指标规范文档。

### [ ] M3 阶段：终稿与项目归档（第 15 周）
* 整合前期计量证据链，提交终版学术综述（Mini Review）稿件。
* 代码整理与注释归档，确保所有网络图谱 100% 可复现。
