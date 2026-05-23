# 📋 项目更新日志 (Project Change Log)

本项目记录“大模型多智能体文献计量分析”任务的所有关键迭代，确保研究的可追溯性。

---

## [v1.0-m3-final] - 2026-05-23 (M3 终稿与可复现 Release)
### 核心交付
- 完成 `paper/mini_review_final.md`，形成课程 mini review 终稿。
- 完成 `reports/m3_final_report.md`，汇总 M1-M3 交付物、核心结果与复现方式。
- 新增 `RELEASE_NOTES.md` 与 `data/README.md`，补齐 GitHub 提交说明和数据说明。
- 重构 `README.md` 为最终提交版本，展示核心结论、图表、仓库结构和复现命令。

### 功能改动
- 新增 `run_pipeline.py`，提供一键复现入口。
- 新增 `src/milestone_papers.py`，生成 Top 10 高被引 milestone 候选论文表。
- 新增 `src/polished_m2_figures.py`，生成提交级 M2 图表。
- 修复关键词共现自连边问题，单篇文献内关键词先标准化去重。
- 修复作者统计中的 `null null` 等无效作者污染。
- 移除词云脚本运行时下载停用词的网络依赖。

---

## [v1.2.0] - 2026-03-29 (M1 收官与结构优化)
### 🏗️ 架构重构 (Refactor)
- **路径规范化**：将数据质检报告移动至 `reports/` 根目录，删除多余的 `data/` 子文件夹。
- **环境隔离**：新增 `requirements.txt`，锁定 pandas(1.5.0+)、matplotlib(3.5.0+) 等核心依赖版本。
- **清理冗余**：移除已填充内容文件夹中的 `.gitkeep` 占位文件，精简仓库体积。

### 📝 文档增强 (Docs)
- **首页升级**：重构 `README.md`，增加项目 Badges、快速启动说明及 M2 Roadmap。
- **日志整合**：新增根目录 `CHANGELOG.md`，合并原有的检索式变更记录。

---

## [v1.1.0] - 2026-03-26 (数据清洗与可视化)
### 📊 核心产出 (Features)
- **趋势分析**：完成 2020-2026 年发文量时序图绘制，识别出领域自 2024 年起的指数级增长。
- **词频图谱**：生成关键词云图，识别出 **Multi-Agent Systems** 与 **Human-AI Interaction** 为当前研究热点。
- **PRISMA 报告**：产出 `data_quality.md`，详细记录 542 篇原始文献去重至 522 篇的筛选逻辑。

### 🔍 检索迭代 (Query History)
- **v2 修改**：在原始检索式中增加了 `Autonomous Agents` 与 `Workflow` 关键词，提升查全率。
- **v1 初始化**：建立 Lens.org 基础检索式，配置导出字段（Title, Year, Abstract, DOI）。

---

## [v1.0.0] - 2026-03-22 (项目启动)
### 🚀 基础建设
- **仓库初始化**：建立标准的数据科学项目结构 (`src/`, `data/`, `outputs/`, `reports/`)。
- **脚本开发**：完成 `src/data_quality.py` 初版，支持自动化数据去重与缺失值统计。

---

> "Quality is not an act, it is a habit." —— 迈向 M2 阶段！
