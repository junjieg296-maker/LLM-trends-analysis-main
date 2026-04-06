# 🚀 基于文献计量学的大语言模型多智能体协作 (LLM Multi-Agent) 前沿趋势追踪

![Status](https://img.shields.io/badge/Status-M1_Completed-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Data](https://img.shields.io/badge/Data_Source-Lens.org-blueviolet?style=flat-square)

本项目为《文献计量学、前沿趋势追踪与项目制学习框架》课程的阶段性开源产出。

本项目严格落实“项目制·可复现”的核心学术要求，绝不使用“随便试出来”的参数或黑盒操作。我们旨在通过对**大语言模型多智能体协作 (LLM Multi-Agent Collaboration)** 领域的学术文献进行系统性的检索、清洗、计量分析与图谱可视化。项目尤其关注 **LLM 智能体在垂直硬核领域的交叉应用（如硬件 EDA、RTL/Verilog 代码生成与测试）**，旨在精准刻画该技术从“通用文本生成”向“复杂工程协作”演化的脉络，并发掘未来高价值的研究空白。

---

## 🛠️ 核心技术栈与工具链 (Tech Stack)

* **数据来源**：[Lens.org](https://www.lens.org/) (保障全字段覆盖率与高信度学术源)
* **数据清洗与分析**：`Python 3.11`, `Pandas` (提供高效的向量化去重与缺失值处理)
* **可视化引擎**：`Matplotlib` (时序分析), `WordCloud` (语义分析)
* **知识图谱 (M2规划)**：`NetworkX`, `VOSviewer` (网络拓扑构建与共现图谱渲染)
* **工程协同**：`Git` & `GitHub Desktop` (全流程版本控制)

---

## 👥 团队成员与精细化分工

为确保分析全流程的可追溯性，团队 5 名成员按照文献计量的标准流水线进行了严格职责划分：

| 姓名 | 角色 | 核心工作内容与阶段性产出 (M1 进度) | 负责目录 |
| :--- | :--- | :--- | :--- |
| **[高俊杰]** | **组长 / 架构统筹** | 搭建项目多级目录，配置 `requirements.txt`。制定 `.gitignore` 规则，坚决贯彻“原始数据不上云”。统筹进度，编写 `src/data_quality.py` 自动化质检脚本。 | `src/`<br>根目录配置 |
| **[赵世铎]** | **数据获取与检索规划** | 维护 `config/query.yaml`，确立 `(Object) AND (Method)` v0.1 检索逻辑。在 Lens.org 规范导出 2020-2026 年间 542 篇包含全字段的原始数据，维护检索变更日志。 | `config/`<br>`data/raw/` |
| **[解明昊]** | **数据清洗与质量管控** | 制定清洗规则，利用 Python 脚本对文献进行 DOI 和标题维度的精准去重。自动化统计字段缺失率（标题完整率100%）。封存清洗后的 522 篇高纯度数据集。 | `data/processed/`<br>`reports/` |
| **[杨广宸]** | **图谱构建与计量分析** | 完成 M1 阶段 2020-2026 发文量指数级增长趋势图及核心词云绘制。撰写 M2 图数据模型设计草图，筹备 VOSviewer/NetworkX 工具链。 | `outputs/`<br>`docs/` |
| **[罗博伟]** | **文献筛选与学术写作** | 严格执行 PRISMA 规范，为剔除的文献记录明确代码。基于 M1 词云，提取前沿洞察，主笔查新对比报告（发掘大模型在 RTL/Verilog 等底层硬件系统中的应用空白）。 | `reports/`<br>`paper/` |

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
