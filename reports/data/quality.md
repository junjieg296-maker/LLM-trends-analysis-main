# M1 里程碑：数据采集与质量评估报告

## 1. 检索概况
* **检索平台**：Lens.org (Scholarly Works)
* **检索日期**：2026-03-26
* **检索式**：`("Large Language Model*" OR "LLM*" OR "Generative AI" OR "Foundation Model*") AND ("Multi-agent*" OR "Collaboration" OR "Coordination" OR "Cooperation" OR "Swarm intelligence") AND ("Autonomous agent*" OR "Agentic workflow" OR "Task planning")`
* **原始数据量**：542 篇

## 2. 数据清洗结果 (Python 自动化处理)
通过运行 `src/data_quality.py` 脚本，清洗结果如下：
* **去重后总记录数**：522 篇
* **重复记录比例**：3.69%
* **核心字段完整度**：
    * Title (标题): 100%
    * Author/s (作者): 99.62%
    * Abstract (摘要): 98.28%
    * References (参考文献): 81.99% (满足共被引分析要求)

## 3. 初步研究发现 (M1 Insight)
通过对 522 篇去重文献的初步可视化分析，得出以下结论：

### A. 发文趋势：指数级增长
![发文趋势图](../outputs/figures/publication_trend.png)
* **解读**：领域自 2023 年起进入爆发期，2025 年发文量（344 篇）呈现陡峭上升趋势，证明该方向是当前的学术前沿热点。

### B. 核心关键词：研究重心转移
![词云图](../outputs/figures/wordcloud_titles.png)
* **系统化**：以 **Multi-Agent Systems** 为核心，探讨复杂任务的协同架构。
* **人性化**：**Human** 关键词的高度凸显，表明“人机协作”是当前研究的重中之重。
* **能力化**：**Autonomous**、**Planning** 与 **Workflow** 的高频出现，印证了研究重心正从“文本生成”向“任务执行”快速转移。

---
**结论**：本项目数据集质量极高，字段完整，趋势明确，具备进入 M2 阶段进行深度引文分析和聚类研究的基础。