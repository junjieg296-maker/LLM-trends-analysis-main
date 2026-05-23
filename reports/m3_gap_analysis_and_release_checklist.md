# M3 课程要求对照与项目完善报告

## 1. 课程项目硬性要求提炼

根据课程 Lesson 1 & 2 课件，课程项目采用"项目制、可复现"框架。主线任务为：

1. Fork/Clone 一个开源项目或自带可运行项目。
2. 跑通项目并读懂关键模块。
3. 完成至少 1 个可验收的功能性改动。
4. 输出可复现分析报告。
5. 完成 6-8 页 mini review。
6. 在期末进行学术报告与答辩。

成绩结构为：课堂考勤与参与 20%，综述实践与项目过程 60%，结果汇报 20%。其中综述实践细分为 M1、M2、M3 三个里程碑，各占 20 分/60 分。M3 的重点是"终稿与可复现 Release"。

## 2. 当前项目完成度

| 课程要求 | 当前状态 | 证据文件 | 评价 |
|---|---|---|---|
| 数据来源与检索式固定 | 已完成 | `config/query.yaml`, `reports/query_changelog.md` | 已记录 Lens.org、时间窗、文献类型和关键词组合 |
| 数据清洗与筛选链条 | 已完成 | `src/data_quality.py`, `reports/m1_data_quality_report.md` | 542 条原始记录清洗为 522 条有效记录 |
| 可复现依赖 | 已补齐 | `requirements.txt` | 原 README 提到但仓库缺失，现已补齐 |
| 一键运行命令 | 已补齐 | `run_pipeline.py` | 可用 `python run_pipeline.py` 复现 M1/M2 主要输出 |
| 计量分析产出 | 已完成 | `src/metrics_analysis.py`, `reports/m2_metrics_analysis_report.md` | 包含发文趋势、被引、h 指数、期刊、作者、领域分布 |
| 3 图 1 表 | 已补强 | `outputs/figures/`, `outputs/milestone_paper_candidates.md`, `reports/m2_metrics_analysis_report.md` | 已有发文趋势、关键词共现、作者合作/机构网络，并新增 Top 10 milestone 候选论文表 |
| 参数记录与敏感性 | 已完成 | `reports/metrics_specification.md`, `outputs/sensitivity_analysis_report.txt` | 记录阈值、时间窗口和节点过滤敏感性 |
| 功能性改动 | 已补齐 | `src/keyword_cooccurrence.py`, `src/metrics_analysis.py`, `run_pipeline.py` | 修复关键词自连边、作者空值污染，并新增流水线 |
| mini review 初稿 | 已补齐 | `paper/mini_review_draft.md` | 按课程蓝本组织为 Introduction、Methods、Results、Discussion |
| Release 归档说明 | 待最终提交时完成 | 建议 GitHub Release v1.0 | 需在 GitHub 页面创建 release/tag |

## 3. 已发现并修复的不足

### 3.1 缺少 `requirements.txt`

README 中声明使用 `pip install -r requirements.txt`，但仓库根目录原本没有该文件。这会直接影响课程强调的"依赖版本锁定"和"一键复现"。现已补充核心依赖：`pandas`、`numpy`、`scipy`、`networkx`、`matplotlib`、`seaborn`、`wordcloud`、`pypdf`。

### 3.2 缺少一键运行入口

课程要求明确提出提供 `python run_pipeline.py` 或 `make report` 形式的一键运行命令。原项目需要分别运行多个脚本，复现路径不够清晰。现已新增 `run_pipeline.py`，顺序执行数据质检、趋势图、词云、计量指标、关键词共现、作者合作、机构网络、引用网络和敏感性分析。

### 3.3 关键词共现存在自连边

`outputs/keyword_statistics.txt` 中曾出现 `artificial intelligence ↔ artificial intelligence`，说明同一篇文献内的重复关键词未先去重。该问题会影响关键词共现边权，尤其会夸大高频通用词的重要性。现已在 `src/keyword_cooccurrence.py` 中增加单篇文献内关键词标准化与去重逻辑，并过滤自连边。

### 3.4 作者统计受到空值污染

`outputs/metrics_summary.txt` 的高产作者 TOP10 中曾出现 `null null`，这说明作者字段中的占位空值进入了统计结果。现已在 `src/metrics_analysis.py` 与 `src/network_analysis.py` 中增加作者清洗逻辑，过滤 `null`、`null null`、`nan`、`unknown` 等无效名称。

### 3.5 词云脚本依赖运行时下载

原 `src/word_cloud_analysis.py` 会在本地缺少 NLTK 停用词时尝试下载，这与课程中的"固定软件依赖、可复现"目标存在冲突。现已移除运行时下载逻辑，改用 `wordcloud` 自带停用词和项目自定义停用词，减少现场复现风险。

## 4. 仍可进一步完善的方向

1. 增加 `data/README.md`，记录原始数据导出日期、Lens.org 字段说明、数据快照口径和隐私说明。
2. 若时间允许，用 CiteSpace 或 VOSviewer 补充共被引聚类/突现词图，因为课程案例明确强调"共被引 + 突现 + 结构变异"对 milestone 识别更有力。
3. 在 GitHub 创建 `v1.0-m3-release`，Release 说明中列出数据版本、运行命令和主要输出。
4. 为期末汇报准备 8-10 页 PPT：研究问题、数据与方法、3 图 1 表、核心发现、局限、未来方向、团队分工。

## 5. M3 提交建议

建议最终提交时重点展示以下证据链：

1. 数据链：`config/query.yaml` -> `data/raw/` -> `src/data_quality.py` -> `data/processed/cleaned_data.csv`
2. 方法链：`reports/metrics_specification.md` -> `run_pipeline.py` -> `outputs/sensitivity_analysis_report.txt`
3. 结果链：`outputs/figures/publication_trend.png`、`keyword_cooccurrence_network.png`、`author_collaboration_network.png`、`institution_country_network.png`
4. 写作链：`reports/m1_data_quality_report.md`、`reports/m2_metrics_analysis_report.md`、`paper/mini_review_draft.md`

这样可以同时覆盖课程中的"可复现代码、可解释结论、参数记录、mini review、最终 Release"五类关键评分点。
