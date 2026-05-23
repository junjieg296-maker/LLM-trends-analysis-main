# 数据说明

## 数据来源

本项目数据来自 Lens.org Scholarly Works，用于分析大语言模型多智能体协作（LLM Multi-Agent Collaboration）相关研究的文献计量特征。

## 检索口径

检索式采用 `(Object) AND (Method)` 的布尔逻辑，具体配置见 `../config/query.yaml`。

Object 词组：

- Large Language Model*
- LLM*
- Generative AI
- Foundation Model*
- ChatGPT

Method 词组：

- Multi-agent*
- Collaboration
- Coordination
- Cooperation
- Multi-agent system*

限定条件：

- 时间范围：2020-2026
- 文献类型：Article, Review, Conference Paper
- 语言：English

## 数据文件

| 文件 | 说明 |
|---|---|
| `raw/lens-llm-agents-raw.csv` | Lens.org 原始导出数据，共 542 条记录 |
| `processed/cleaned_data.csv` | 经 DOI 与 Title 去重后的清洗数据，共 522 条记录 |

## 清洗规则

数据清洗脚本为 `../src/data_quality.py`。清洗规则如下：

1. 读取原始 CSV 文件。
2. 去除字段名中的空格。
3. 基于 DOI 去重。
4. 基于 Title 再次去重。
5. 输出清洗后数据到 `processed/cleaned_data.csv`。

## 字段质量

清洗后数据字段质量如下：

| 字段 | 缺失率 |
|---|---:|
| Title | 0.00% |
| Author/s | 0.38% |
| Abstract | 1.72% |
| References | 18.01% |
| DOI | 0.19% |

## 复现方式

在项目根目录运行：

```bash
python src/data_quality.py
```

或运行完整流水线：

```bash
python run_pipeline.py
```
