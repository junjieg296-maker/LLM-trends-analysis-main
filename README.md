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

## GitHub 巡检材料导航

根据 Lesson 27 & 28 的最终成果包要求，本项目已补齐以下巡检入口：

| 课程检查项 | 本项目路径 | 说明 |
|---|---|---|
| 课程论文 | `paper/course_paper_cn.pdf`, `paper/mini_review_final.md` | 中文版课程论文和 mini review 终稿 |
| GitHub 仓库说明 | `README.md` | 研究主题、成员分工、数据来源、运行命令、输出目录 |
| 数据与筛选记录 | `data/README.md`, `data/field_dictionary.md`, `data/screening_records.csv` | 数据来源、字段字典、542 -> 522 筛选流程 |
| 检索式 | `config/query.yaml` | Query as Code |
| 参数说明 | `params.md` | 时间窗、阈值、Top N、共现阈值等参数选择理由 |
| 代码复现 | `run_pipeline.py`, `requirements.txt` | 一键运行核心分析流程 |
| 3 图 1 表 | README 中“课程要求版：3 图 1 表对应关系”；`outputs/tables/top_cited_papers.md` | Fig.1/Fig.2/Fig.3/Table 1 与 RQ 绑定 |
| AI 使用说明 | `docs/ai_usage.md` | 工具用途、人工核验方式与使用边界 |
| 答辩材料 | `presentation/LLM_multi_agentpptx.pptx` | 最新版答辩 PPT |
| 小组分工与个人反思 | `reflection/team_division/team_division.md`, `reflection/*/reflection.md` | 小组分工说明、各成员第一人称收获与反思；高俊杰为主要统筹与最终整合贡献者 |

---

## 团队成员与任务分工

本项目采用“数据获取 - 数据清洗 - 计量分析 - 图谱构建 - 综述写作 - 工程归档”的流水线式分工。每位成员的工作都绑定到具体目录、脚本、报告或图表，便于在 GitHub 中追踪贡献。

| 成员 | 项目角色 | 主要负责内容 | 对应交付物 |
|---|---|---|---|
| 高俊杰 | 组长 / 项目统筹 / 工程整合 / 最终提交负责人 | 负责确定项目主题和研究范围，梳理课程要求并拆分为 M1、M2、M3 任务；设计 GitHub 仓库目录结构，整理 `config/`、`data/`、`src/`、`outputs/`、`reports/`、`paper/`、`presentation/` 和 `reflection/`；维护 `run_pipeline.py` 一键复现入口和 `requirements.txt` 依赖说明；检查并整合数据清洗、指标计算、关键词共现、合作网络、引用网络和共被引网络等分析脚本；多次重写 README，补充数据来源、筛选流程、字段说明、RQ、3 图 1 表、高被引文献表、图表解释、复现命令和课程交付物；整理 M1-M3 阶段报告，修订 M2 图表说明和 paper 图文逻辑；补齐 `docs/ai_usage.md`、`params.md`、`data/field_dictionary.md`、`data/screening_records.csv`、`outputs/tables/`、`reflection/` 和答辩 PPT 归档；负责最终提交前的仓库巡检和材料完整性检查。 | `README.md`、`run_pipeline.py`、`requirements.txt`、`params.md`、`docs/ai_usage.md`、`data/field_dictionary.md`、`data/screening_records.csv`、`outputs/tables/`、`reports/`、`paper/`、`presentation/`、`reflection/` |
| 赵世铎 | 数据获取与检索策略规划 | 负责 Lens.org 检索策略设计，围绕 `(Object) AND (Method)` 逻辑确定关键词组合、时间范围、文献类型和语言限制；记录检索口径与策略变化。 | `config/query.yaml`、`data/raw/lens-llm-agents-raw.csv`、`reports/query_changelog.md`、`CHANGELOG.md` |
| 解明昊 | 数据清洗与质量控制 | 负责原始数据去重、字段标准化、缺失值检查和质量评估；基于 DOI 与 Title 双重去重，将 542 条原始记录清洗为 522 篇有效文献。 | `data/processed/cleaned_data.csv`、`src/data_quality.py`、`reports/m1_data_quality_report.md` |
| 杨广宸 | 计量分析与知识图谱构建 | 负责年度趋势、关键词共现、作者合作、机构/国家分布、引用网络、共被引网络和参数敏感性分析；输出 M2 阶段核心图表和指标结果。 | `src/metrics_analysis.py`、`src/keyword_cooccurrence.py`、`src/network_analysis.py`、`src/sensitivity_analysis.py`、`outputs/figures/`、`outputs/sensitivity_analysis_report.txt` |
| 罗博伟 | 文献筛选与综述写作 | 负责将 M1-M2 的计量证据转化为综述结构，整理 milestone 候选论文、主题叙事线、挑战与未来方向；参与 mini review 终稿和答辩材料组织。 | `outputs/milestone_paper_candidates.md`、`paper/mini_review_final.md`、`reports/m3_final_report.md`、`outputs/review_figures/` |

### 分工逻辑

| 阶段 | 小组协作重点 | 主要负责人 |
|---|---|---|
| M1 数据与检索方案 | 检索式设计、原始数据导出、去重清洗、字段质量评估 | 高俊杰统筹，赵世铎、解明昊辅助 |
| M2 计量分析与图谱 | 指标计算、关键词共现、作者合作、机构分布、引用与共被引网络、敏感性分析 | 高俊杰统筹，杨广宸辅助 |
| M3 综述与项目归档 | milestone 论文识别、mini review 写作、图文解释、release 报告、答辩 PPT | 高俊杰统筹，罗博伟和全组辅助 |

完整小组分工见：`reflection/team_division/team_division.md`。各成员第一人称个人收获与反思见：`reflection/gao_junjie/reflection.md`、`reflection/zhao_shiduo/reflection.md`、`reflection/xie_minghao/reflection.md`、`reflection/yang_guangchen/reflection.md`、`reflection/luo_bowei/reflection.md`。

---

## 研究问题与图表证据对应

根据 Lesson 21-22 中对文献计量型 Review 的要求，综述问题（Research Questions, RQs）不能只是宽泛主题，而必须满足以下条件：

| 课程要求 | 本项目落实方式 |
|---|---|
| RQ 不能过大、过虚 | 每个 RQ 都限定到“发展态势、合作主体、主题热点、知识基础、研究空白”等可分析对象 |
| RQ 必须能被图表、指标或代表文献回答 | 每个 RQ 都绑定至少一张图表、关键指标和解释边界 |
| 图表不能为了插图而插图 | 每张图都明确回答哪个 RQ，并说明“能说明什么”和“不能推出什么” |
| Results 段落要围绕一个 Claim 展开 | 每个 RQ 都对应一个核心发现，用于后续 Results / Discussion 写作 |

### RQ 总览表

| RQ | 具体研究问题 | 分析方法 | 主要图表 / 证据 | 关键指标 |
|---|---|---|---|---|
| RQ1 | 2020-2026 年 LLM 多智能体协作研究的发文量如何变化？该领域处于什么发展阶段？ | 年度发文统计、增长率分析、影响力指标 | 年度发文阶段图、指标汇总 | 年发文量、增长率、总被引、h 指数 |
| RQ2 | 该领域的核心研究主体和合作格局是什么？是否已经形成稳定核心团队？ | 作者合作网络、机构 / 国家分布分析 | 作者合作网络、机构 / 国家分布图 | 作者数、篇均作者数、合作网络节点与边 |
| RQ3 | 该领域的研究热点集中在哪些主题？这些主题之间形成了怎样的技术结构？ | 关键词共现、主题归纳 | 关键词共现网络、主题架构图 | 高频关键词、共现强度、主题层次 |
| RQ4 | 哪些高影响论文构成该领域的知识基础？这些论文如何支撑综述中的技术叙事线？ | 高被引论文识别、引用 / 共被引分析 | milestone 候选矩阵、文献共被引网络 | 被引次数、共被引关系、主题簇 |
| RQ5 | 基于计量结果和代表文献，该领域仍存在哪些研究空白和未来挑战？ | 证据链归纳、Discussion 趋势总结 | 挑战与未来研究议程图 | 评价体系、可解释性、场景验证、安全治理 |

### 课程要求版：3 图 1 表对应关系

按照 Lesson 21-22 的要求，3 图 1 表不能只是“做出来”，而要分别回答明确的综述问题。本项目将核心图表组织如下：

| 类型 | 图表编号 | 图表名称 | 回答的 RQ | 关键指标 / 读图重点 | 写入位置 |
|---|---|---|---|---|---|
| 图 | Fig. 1 | 年度发文增长与发展阶段图 | RQ1：发展态势如何？ | 年发文量、增长率、2024-2025 爆发窗口 | Results 3.1 |
| 图 | Fig. 2 | 作者合作网络图 | RQ2：核心主体与合作格局是什么？ | 节点、边、重复合作关系、合作网络分散程度 | Results 3.2 |
| 图 | Fig. 3 | 关键词共现与主题结构图 | RQ3：研究热点集中在哪些主题？ | 高频关键词、共现关系、主题层次 | Results 3.3 |
| 表 | Table 1 | Top 10 高被引文献表 | RQ4：知识基础是什么？ | 被引次数、年份、来源、主题归属 | Results 3.4 |

其中 **Table 1 Top 10 高被引文献表** 是本项目回答 RQ4 的核心表格。它不是简单列论文，而是用于识别该领域的 milestone 候选文献，并进一步支撑综述中的四条技术叙事线。表格文件同时保存在 `outputs/tables/top_cited_papers.md` 和 `outputs/tables/top_cited_papers.csv`，便于 GitHub 巡检和后续复现。

---

### RQ1：2020-2026 年 LLM 多智能体协作研究的发文量如何变化？该领域处于什么发展阶段？

**对应图表：年度发文增长与发展阶段图**

![Publication growth and development stages](outputs/review_figures/fig2_publication_growth_stages.png)

**分析方法与关键指标**

| 指标 | 结果 |
|---|---:|
| 2020 年发文量 | 1 篇 |
| 2024 年发文量 | 81 篇 |
| 2025 年发文量 | 344 篇 |
| 平均年增长率 | 181.29% |
| 总被引次数 | 4,265 |
| h 指数 | 31 |

**解释说明**

RQ1 关注的是领域发展态势。年度发文量显示，LLM 多智能体协作研究并不是线性增长，而是经历了明显的阶段变化：2020-2023 年文献数量较少，属于早期探索阶段；2024 年发文量上升到 81 篇，说明 agentic AI、工具调用、RAG 和自动化工作流开始成为独立研究热点；2025 年发文量进一步达到 344 篇，表明该领域进入爆发式增长阶段。

影响力指标进一步补充了这一判断。总被引次数达到 4,265 次，h 指数为 31，说明该领域不仅有大量新文献出现，也已经形成一批具有较高影响力的基础研究和代表性论文。与此同时，被引中位数较低、零被引论文较多，说明大量新近论文仍处于引用积累早期。

**边界说明**

该图能够说明“文献层面的关注度和研究活动显著增加”，但不能直接推出“技术已经成熟”或“应用已经充分落地”。此外，2026 年数据尚未覆盖全年，因此不能与完整年份直接比较。

---

### RQ2：该领域的核心研究主体和合作格局是什么？是否已经形成稳定核心团队？

**对应图表：作者合作网络**

![Author collaboration network](outputs/figures/author_collaboration_network.png)

**辅助图表：机构 / 国家分布网络**

![Institution and country network](outputs/figures/institution_country_network.png)

**分析方法与关键指标**

| 指标 | 结果 |
|---|---:|
| 作者总数 | 约 2,564-2,565 人 |
| 篇均作者数 | 约 5.07-5.10 人 |
| 作者合作原始网络 | 2,502 个节点，12,227 条边 |
| 合作阈值过滤后网络 | 51 个节点，48 条边 |
| 最高产作者发文量 | 3 篇 |

**解释说明**

RQ2 关注的是“谁在研究这个领域”以及“研究力量是否已经集中”。作者合作网络显示，LLM 多智能体协作研究虽然涉及作者数量较多，但稳定重复合作关系并不密集。将一次性合作过滤后，网络只保留 51 个节点和 48 条边，说明当前研究仍以小团队、项目型合作和新进入者为主，尚未形成高度集中的核心作者群体。

机构 / 国家分布图进一步说明该领域具有明显跨区域和跨学科特征。北美、欧洲和亚洲均有研究力量参与，研究来源覆盖人工智能、机器人、人机交互、医学、工程系统等多个方向。这与 LLM 多智能体协作本身的系统属性一致：它不是单一模型技术，而是涉及模型、工具、任务环境和应用场景的综合问题。

**边界说明**

作者合作图能够说明合作结构和重复合作关系，但不能直接评价某个作者或机构的研究质量。机构 / 国家信息也可能受到 Lens.org 元数据字段缺失或格式差异影响，因此本项目更谨慎地将其解释为“研究力量分布线索”，而不是绝对排名。

---

### RQ3：该领域的研究热点集中在哪些主题？这些主题之间形成了怎样的技术结构？

**对应图表：关键词共现网络**

![Keyword co-occurrence network](outputs/figures/keyword_cooccurrence_network.png)

**辅助图表：主题架构图**

![Thematic architecture of LLM multi-agent collaboration](outputs/review_figures/fig3_thematic_architecture.png)

**分析方法与关键指标**

| 指标 | 结果 |
|---|---:|
| 关键词共现网络节点数 | 227 个关键词 |
| 关键词共现网络边数 | 2,087 条共现关系 |
| 共现过滤阈值 | 共现频次 >= 2 |
| 高频关键词 1 | `artificial intelligence`，56 次 |
| 高频关键词 2 | `large language models`，45 次 |
| 高频关键词 3 | `large language model`，24 次 |

**解释说明**

RQ3 关注的是“研究热点是什么”。关键词共现网络显示，该领域的研究主题并不是随机分散，而是围绕若干技术层次展开。结合高频关键词和主题架构图，本项目将 LLM 多智能体协作研究归纳为四个层次：

| 主题层次 | 代表关键词 | 含义 |
|---|---|---|
| 技术底座 | `large language models`, `artificial intelligence`, `machine learning`, `NLP` | 多智能体系统仍依赖 LLM 和 AI 基础能力 |
| 协作架构 | `agentic ai`, `multi-agent systems`, `ai agents` | 研究重点从单模型输出转向角色分工、任务拆解和多智能体协作 |
| 能力增强 | `retrieval-augmented generation`, `reinforcement learning`, `planning` | 关注知识检索、工具调用、反馈学习和复杂规划 |
| 治理应用 | `ethics`, `human-robot interaction`, `digital health`, `robot` | 多智能体系统进入高约束应用和安全治理场景 |

这说明 LLM 多智能体协作研究的核心不是简单“增加几个智能体”，而是围绕任务组织方式、智能体通信机制、工具调用、证据检索、人类监督和垂直场景落地展开。

**边界说明**

关键词共现图能够说明文献中的高频主题和主题关联，但不能直接证明某个技术方向“已经成熟”或“必然成为未来主流”。它反映的是文献层面的关注度和结构，而不是技术效果的最终评价。

---

### RQ4：哪些高影响论文构成该领域的知识基础？这些论文如何支撑综述中的技术叙事线？

**对应图表：milestone 候选矩阵**

![Milestone candidate matrix](outputs/review_figures/fig4_milestone_roadmap.png)

**辅助图表：文献共被引网络**

![Reference co-citation network](outputs/review_figures/fig6_reference_cocitation_network.png)

**分析方法与关键指标**

| 分析对象 | 方法 | 指标 |
|---|---|---|
| 高影响论文 | 按 Lens.org 被引次数排序 | Citing Works Count |
| milestone 候选论文 | Top 10 高被引论文筛选 | 年份、被引次数、主题归属 |
| 共被引关系 | 统计文献被共同引用的关系 | 共被引强度、主题簇 |
| 综述技术主线 | 将高被引论文与关键词主题结合 | 任务规划、科学发现、人机协作、医疗 / 机器人 |

**Table 1. Top 10 高被引文献表**

以下表格按 Lens.org 的 Citing Works Count 排序，用于识别本研究语料中的第一轮 milestone 候选文献。该表对应课程要求中的 “1 表”，并与 RQ4 直接绑定。

| Rank | Year | Citations | Title | Source | DOI |
|---:|---:|---:|---|---|---|
| 1 | 2024 | 352 | Self-Driving Laboratories for Chemistry and Materials Science. | Chemical Reviews | `10.1021/acs.chemrev.4c00055` |
| 2 | 2023 | 259 | A Comprehensive Review of Recent Research Trends on Unmanned Aerial Vehicles (UAVs) | Systems | `10.3390/systems11080400` |
| 3 | 2023 | 173 | Co-Writing Screenplays and Theatre Scripts with Language Models: Evaluation by Industry Professionals | CHI Conference on Human Factors in Computing Systems | `10.1145/3544548.3581225` |
| 4 | 2025 | 136 | A review of large language models and autonomous agents in chemistry. | Chemical Science | `10.1039/d4sc03921a` |
| 5 | 2024 | 109 | SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models | IEEE/RSJ IROS | `10.1109/iros58592.2024.10802322` |
| 6 | 2024 | 108 | Evaluating large language models as agents in the clinic. | NPJ Digital Medicine | `10.1038/s41746-024-01083-y` |
| 7 | 2023 | 104 | Defining human-AI teaming the human-centered way: a scoping review and network analysis. | Frontiers in Artificial Intelligence | `10.3389/frai.2023.1250725` |
| 8 | 2024 | 101 | RoCo: Dialectic Multi-Robot Collaboration with Large Language Models | IEEE ICRA | `10.1109/icra57147.2024.10610855` |
| 9 | 2024 | 100 | Understanding Large-Language Model (LLM)-powered Human-Robot Interaction | ACM/IEEE HRI | `10.1145/3610977.3634966` |
| 10 | 2024 | 90 | The impact of large language models on radiology: a guide for radiologists on the latest innovations in AI. | Japanese Journal of Radiology | `10.1007/s11604-024-01552-0` |

表格数据文件见：`outputs/milestone_paper_candidates.md`。

**解释说明**

RQ4 关注的是“知识基础是什么”。milestone 候选矩阵先回答“哪些论文在该领域更具影响力”，共被引网络进一步回答“这些论文背后如何形成共同知识基础”。两者结合可以避免综述写成论文清单，而是把代表性论文组织成技术叙事线。

基于高被引论文和主题图谱，本项目将综述主体归纳为四条技术主线：

1. **多智能体任务规划与自动化工作流**：关注自然语言目标如何被拆分为可执行子任务，并由多个智能体协作完成。
2. **科学发现与自驱动实验室**：关注 LLM agent 在文献检索、假设生成、实验设计和结果分析中的闭环作用。
3. **人机协作与人类监督**：关注多智能体系统中人类如何参与监督、纠错、责任承担和最终决策。
4. **医疗、机器人等垂直行业智能体**：关注高约束场景中的证据、安全、审计和失败恢复机制。

**边界说明**

被引次数高不等于论文结论一定正确，也不等于技术路线已经成熟。高被引论文更适合作为“知识基础和代表性文献”的线索，仍需要结合论文内容、主题位置和共被引关系进行解释。

---

### RQ5：基于计量结果和代表文献，该领域仍存在哪些研究空白和未来挑战？

**对应图表：挑战与未来研究议程图**

![Challenges and future research agenda](outputs/review_figures/fig5_challenges_agenda.png)

**分析方法与证据来源**

RQ5 不是凭主观判断提出未来方向，而是综合 RQ1-RQ4 的结果进行归纳：

| 证据来源 | 支撑的挑战 |
|---|---|
| 发文量快速增长但零被引论文较多 | 领域快速扩张，评价体系和知识沉淀仍在形成 |
| 作者合作网络较分散 | 稳定共同体和标准化基准尚未完全形成 |
| 关键词中出现 RAG、RL、ethics、HRI、digital health | 能力增强、安全治理和垂直应用成为重要议题 |
| milestone 与共被引网络显示多主题并行 | 领域尚未形成单一主导范式，需要更清晰的技术分类和证据链 |

**解释说明**

本项目将未来挑战归纳为四个方向：

1. **评价体系不统一**：不同论文使用不同任务、智能体数量、提示词、工具环境和评价标准，导致横向比较困难。
2. **协作机制可解释性不足**：多智能体系统完成任务后，仍需要说明任务如何分配、冲突如何解决、错误来自哪个环节。
3. **垂直场景验证有限**：医疗、机器人、科学实验和工程设计等场景需要更强的约束、审计和专家验证。
4. **安全治理更加复杂**：多智能体系统可能出现错误传播、责任模糊、工具误用和人类监督不足等问题。

**边界说明**

RQ5 的结论属于 Discussion 层面的趋势归纳，不能写成“未来必然如何”。更稳妥的表达是：现有文献显示这些问题正在受到关注，并可能成为后续研究需要重点解决的方向。

---

## 核心发现摘要

基于对 522 篇文献的计量分析，本项目形成以下核心发现：

### 📈 发展阶段判断
- **爆发期已至**：2024-2025 年发文量呈指数级增长（2025年达 344 篇，同比增长 325%），领域从早期探索进入高速扩张阶段
- **影响力初显**：总被引 4,265 次，h 指数 31，已形成稳定的高影响论文基础

### 👥 研究主体特征
- **高度分散**：作者合作网络过滤一次性合作后仅余 51 个节点，尚未形成集中的核心团队
- **跨域协作**：覆盖 AI、机器人、人机交互、医学等多个学科，开放获取比例达 73.18%

### 🔍 主题结构框架
- **四层技术体系**：技术底座（LLM/AI）→ 协作架构（agentic AI）→ 能力增强（RAG/RL/planning）→ 治理应用（ethics/HRI）
- **从"单模型"到"系统协作"**：研究重心已转向任务拆解、角色分工和多智能体协同机制

### 📚 知识基础构建
- **四条技术主线**：任务规划与自动化工作流、科学发现与自驱动实验室、人机协作与监督、垂直行业智能体
- **共被引网络支撑叙事**：通过高被引论文识别与共被引分析，将论文清单转化为技术演进叙事

### ⚠️ 未来挑战方向
- 评价体系不统一、协作机制可解释性不足
- 垂直场景验证有限、安全治理复杂化

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
| 字段字典 | `data/field_dictionary.md` |
| 筛选记录 | `data/screening_records.csv` |

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
- `params.md`

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
- `data/field_dictionary.md`
- `data/screening_records.csv`

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

### 核心表格

| 表格 | 文件路径 | 用途 |
|---|---|---|
| Table 1 Top 10 高被引文献表 | `outputs/tables/top_cited_papers.md`, `outputs/tables/top_cited_papers.csv` | 回答 RQ4，识别知识基础与 milestone 候选论文 |

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
│   ├── README.md                           # 数据来源与清洗说明
│   ├── field_dictionary.md                 # 字段字典
│   ├── screening_records.csv               # 筛选记录
│   ├── raw/
│   │   └── lens-llm-agents-raw.csv         # 原始导出数据
│   └── processed/
│       └── cleaned_data.csv                # 清洗去重后的有效数据集
├── docs/
│   ├── graph_data_model.md                 # 知识图谱数据模型说明
│   └── ai_usage.md                         # AI 使用说明
├── outputs/
│   ├── figures/                            # M2 计量分析图表
│   ├── review_figures/                     # 综述和答辩图表
│   ├── tables/                             # 课程要求中的核心表格
│   ├── metrics_summary.txt                 # 指标汇总
│   ├── keyword_statistics.txt              # 关键词统计
│   ├── milestone_paper_candidates.md       # Top 10 milestone 候选论文
│   └── sensitivity_analysis_report.txt     # 参数敏感性分析
├── paper/
│   ├── course_paper_cn.pdf                 # 中文版课程论文
│   └── mini_review_final.md                # 综述终稿 Markdown
├── presentation/
│   ├── README.md
│   └── LLM_multi_agentpptx.pptx
├── reflection/
│   ├── README.md
│   ├── team_division/
│   │   └── team_division.md                # 小组分工与贡献说明
│   ├── gao_junjie/
│   │   └── reflection.md                   # 高俊杰第一人称个人收获与反思
│   ├── zhao_shiduo/
│   │   └── reflection.md                   # 赵世铎第一人称个人收获与反思
│   ├── xie_minghao/
│   │   └── reflection.md                   # 解明昊第一人称个人收获与反思
│   ├── yang_guangchen/
│   │   └── reflection.md                   # 杨广宸第一人称个人收获与反思
│   └── luo_bowei/
│       └── reflection.md                   # 罗博伟第一人称个人收获与反思
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
├── params.md                               # 参数与阈值说明
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
| 中文版课程论文 | `paper/course_paper_cn.pdf` |
| Mini review 终稿 | `paper/mini_review_final.md` |
| 指标规范 | `reports/metrics_specification.md` |
| 关键图表与表格 | `outputs/figures/`, `outputs/review_figures/`, `outputs/tables/` |
| 一键复现入口 | `run_pipeline.py` |
| 参数说明 | `params.md` |
| AI 使用说明 | `docs/ai_usage.md` |
| 小组分工与个人反思 | `reflection/team_division/team_division.md`, `reflection/*/reflection.md` |
| 答辩 PPT | `presentation/LLM_multi_agentpptx.pptx` |

---

## 许可

本项目采用 MIT License，详见 `LICENSE`。
