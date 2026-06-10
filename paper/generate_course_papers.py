from __future__ import annotations

import csv
import os
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"
FIG_DIR = ROOT / "outputs" / "figures"
REVIEW_FIG_DIR = ROOT / "outputs" / "review_figures"
TABLE_DIR = ROOT / "outputs" / "tables"


FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("MSYH", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("MSYH-Bold", FONT_BOLD))


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "PaperTitle",
            parent=base["Title"],
            fontName="MSYH-Bold",
            fontSize=17,
            leading=23,
            alignment=TA_CENTER,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="MSYH",
            fontSize=9.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "abstract_title": ParagraphStyle(
            "AbstractTitle",
            parent=base["Heading2"],
            fontName="MSYH-Bold",
            fontSize=10.5,
            leading=14,
            spaceBefore=4,
            spaceAfter=4,
            textColor=colors.HexColor("#1F2937"),
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "Heading1CJK",
            parent=base["Heading1"],
            fontName="MSYH-Bold",
            fontSize=13.5,
            leading=18,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.HexColor("#17324D"),
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "Heading2CJK",
            parent=base["Heading2"],
            fontName="MSYH-Bold",
            fontSize=11.5,
            leading=15,
            spaceBefore=7,
            spaceAfter=4,
            textColor=colors.HexColor("#234E70"),
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "BodyCJK",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=9.2,
            leading=14.3,
            firstLineIndent=0.5 * cm,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "body_no_indent": ParagraphStyle(
            "BodyNoIndent",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=9.2,
            leading=14.3,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=8.0,
            leading=11,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#374151"),
            spaceBefore=2,
            spaceAfter=7,
            wordWrap="CJK",
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=7.4,
            leading=9.8,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName="MSYH-Bold",
            fontSize=7.1,
            leading=8.8,
            alignment=TA_CENTER,
            textColor=colors.white,
            wordWrap="CJK",
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=6.7,
            leading=8.4,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "note": ParagraphStyle(
            "Note",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=8.1,
            leading=11,
            leftIndent=0.3 * cm,
            rightIndent=0.3 * cm,
            textColor=colors.HexColor("#4B5563"),
            wordWrap="CJK",
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def rich(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def add_paragraphs(story, paragraphs, style):
    for text in paragraphs:
        story.append(p(text, style))


def scaled_image(path: Path, max_width: float = 15.8 * cm, max_height: float = 8.3 * cm) -> Image:
    with PILImage.open(path) as img:
        width, height = img.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width * scale, height * scale)


def short_title(title: str, limit: int = 62) -> str:
    title = " ".join(title.replace("\n", " ").split())
    return title if len(title) <= limit else title[: limit - 3] + "..."


def infer_theme(title: str) -> str:
    low = title.lower()
    if "chem" in low or "laborator" in low or "materials" in low:
        return "Scientific discovery"
    if "robot" in low or "uav" in low:
        return "Robotics / planning"
    if "human" in low or "screenplay" in low or "theatre" in low:
        return "Human-AI collaboration"
    if "clinic" in low or "radiology" in low:
        return "Medical agents"
    return "Agentic workflow"


def load_top_papers():
    rows = []
    with open(TABLE_DIR / "top_cited_papers.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            rows.append(
                {
                    "rank": idx,
                    "year": row.get("Publication Year", ""),
                    "citations": row.get("Citing Works Count", ""),
                    "title": row.get("Title", ""),
                    "source": row.get("Source Title", ""),
                    "doi": row.get("DOI", ""),
                    "theme": infer_theme(row.get("Title", "")),
                }
            )
    return rows


def reference_lines(lang: str = "cn"):
    lines = []
    for idx, row in enumerate(load_top_papers(), 1):
        prefix = f"[{idx}]"
        title = row["title"].rstrip(".")
        if lang == "cn":
            lines.append(f"{prefix} {title}. {row['source']}, {row['year']}. DOI: {row['doi']}.")
        else:
            lines.append(f"{prefix} {title}. {row['source']}, {row['year']}. DOI: {row['doi']}.")
    if lang == "cn":
        lines.extend(
            [
                "[11] 本课程项目 GitHub 仓库：LLM-trends-analysis-main，包含检索式、清洗数据、分析脚本、图表输出、参数说明和 AI 使用说明。",
                "[12] Lens.org Scholarly Works 数据导出与项目检索配置：config/query.yaml, data/raw/lens-llm-agents-raw.csv, data/processed/cleaned_data.csv.",
            ]
        )
    else:
        lines.extend(
            [
                "[11] Course GitHub repository: LLM-trends-analysis-main, including query configuration, cleaned data, analysis scripts, output figures, parameter notes, and AI-use statement.",
                "[12] Lens.org Scholarly Works export and project query configuration: config/query.yaml, data/raw/lens-llm-agents-raw.csv, data/processed/cleaned_data.csv.",
            ]
        )
    return lines


def make_table(data, col_widths, style_sheet):
    wrapped = []
    for row_index, row in enumerate(data):
        row_style = style_sheet["table_header"] if row_index == 0 else style_sheet["table_cell"]
        wrapped.append([rich(str(cell), row_style) for cell in row])
    table = Table(wrapped, colWidths=col_widths, repeatRows=1, hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 3.2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3.2),
                ("TOPPADDING", (0, 0), (-1, -1), 3.0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
            ]
        )
    )
    return table


def page_decorator(title: str):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("MSYH", 7)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(doc.leftMargin, 1.05 * cm, title)
        canvas.drawRightString(A4[0] - doc.rightMargin, 1.05 * cm, f"{doc.page}")
        canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
        canvas.line(doc.leftMargin, 1.38 * cm, A4[0] - doc.rightMargin, 1.38 * cm)
        canvas.restoreState()

    return draw


def add_figure(story, path: Path, caption: str, style_sheet, max_height=8.3 * cm):
    story.append(Spacer(1, 4))
    story.append(scaled_image(path, max_height=max_height))
    story.append(rich(f"<b>{escape(caption.split('。')[0] + '。')}</b>{escape(caption[len(caption.split('。')[0]) + 1:])}", style_sheet["caption"]))


def chinese_story(style_sheet):
    story = []
    story.append(p("大语言模型多智能体协作研究的文献计量型 Mini Review：发展态势、知识基础与未来议程", style_sheet["title"]))
    story.append(p("课程论文｜基于 Lens.org 2020-2026 年 522 篇文献的可复现 GitHub 项目", style_sheet["subtitle"]))
    story.append(p("作者：高俊杰、赵世铎、解明昊、杨广宸、罗博伟", style_sheet["subtitle"]))
    story.append(Spacer(1, 6))

    story.append(p("摘要", style_sheet["abstract_title"]))
    add_paragraphs(
        story,
        [
            "大语言模型正在从单模型问答与文本生成工具，转向能够承担任务分解、工具调用、角色协作和复杂流程执行的智能体系统。为系统把握 LLM 多智能体协作研究的知识结构与发展趋势，本文基于 Lens.org Scholarly Works 构建 2020-2026 年文献数据集，经 DOI 与标题去重后获得 522 篇有效文献。本文采用文献计量学方法分析年度发文趋势、作者合作网络、关键词主题结构、高被引代表文献和共被引知识基础，并将图谱证据转化为综述中的技术叙事线。",
            "结果显示，该领域在 2024-2025 年进入快速爆发期，2025 年发文量达到 344 篇；样本总被引次数为 4,265 次，h 指数为 31。作者合作网络显示当前研究力量仍以分散的小团队和项目型协作为主，尚未形成高度稳定的核心作者群。关键词结构显示研究主题可以归纳为 LLM/AI 技术底座、智能体协作架构、RAG/RL 能力增强以及治理与垂直应用四个层次。结合 Top 10 高被引论文和共被引网络，本文进一步将该领域归纳为科学发现与自驱动实验室、机器人任务规划、人机协作、医疗与垂直行业智能体四条主线。本文最后讨论评价体系不统一、协作机制可解释性不足、垂直场景验证有限和安全治理复杂化等挑战。",
        ],
        style_sheet["body_no_indent"],
    )
    story.append(p("关键词：大语言模型；多智能体系统；文献计量学；关键词共现；共被引网络；mini review", style_sheet["note"]))

    story.append(p("1. 引言", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "大语言模型（Large Language Models, LLMs）的快速发展使人工智能系统的能力边界发生了明显变化。早期 LLM 应用主要集中于问答、摘要、翻译、写作辅助和代码生成等单模型任务；随着工具调用、检索增强生成、长上下文推理和函数调用能力的发展，LLM 开始被嵌入更复杂的工作流中，承担规划、检索、执行、评价和反思等角色。在这一背景下，多智能体协作成为 LLM 研究的重要方向。",
            "与单一 LLM 系统相比，多智能体系统的核心并不是简单增加模型数量，而是通过角色分工、消息传递、证据检索、任务拆解和相互检查提升复杂任务处理能力。例如，在软件开发场景中，不同智能体可以分别负责需求分析、架构设计、代码生成、测试和审查；在科学发现中，智能体系统可以参与文献检索、假设生成、实验设计、数据分析和报告撰写；在医疗和机器人场景中，LLM 智能体可以作为高层规划器或辅助决策组件，但也必须接受领域知识、安全边界和人类监督的约束。",
            "这一研究方向增长很快，但也给综述写作带来困难。一方面，新概念、新框架和新应用密集出现，单纯依靠人工经验挑选文献容易造成主题偏差；另一方面，该领域横跨人工智能、机器人、软件工程、医疗健康、化学实验室自动化、人机交互和安全治理等多个方向，传统叙述式综述很难同时说明研究热度、知识基础和技术结构。因此，本文采用文献计量型 mini review 的写法，用可复现数据、图表和代表文献回答明确的研究问题。",
        ],
        style_sheet["body"],
    )

    story.append(p("2. 数据来源与研究方法", style_sheet["h1"]))
    story.append(p("2.1 数据来源、检索式与筛选流程", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "本文数据来自 Lens.org Scholarly Works。检索采用“对象词组（Object）AND 方法词组（Method）”的布尔逻辑：Object 词组包括 Large Language Model*、LLM*、Generative AI、Foundation Model* 和 ChatGPT；Method 词组包括 Multi-agent*、Collaboration、Coordination、Cooperation 和 Multi-agent system*。时间范围设定为 2020-2026 年，文献类型限定为 Article、Review 和 Conference Paper，语言限定为 English。项目检索配置记录于 GitHub 仓库的 config/query.yaml，检索式版本记录显示初始配置建立于 2026-03-26；原始数据文件创建时间同为 2026-03-26，因此本文将该日期作为本课程项目的数据导出与检索记录日期。",
            "原始检索获得 542 条记录。为降低重复记录对计量结果的影响，项目先按 DOI 去重，再按 Title 去重，最终获得 522 篇有效文献。清洗后数据中，Title 和 Publication Year 字段覆盖率为 100%，Abstract 字段覆盖率为 98.28%，References 字段覆盖率为 81.99%，DOI 字段覆盖率为 99.81%。这些字段能够支持年度趋势、关键词共现、作者合作、引用网络、共被引网络和高被引代表文献识别。",
        ],
        style_sheet["body"],
    )

    methods = [
        ["透明度项目", "本文落实方式"],
        ["数据库名称", "Lens.org Scholarly Works"],
        ["完整检索式", "Object AND Method；详见 config/query.yaml"],
        ["检索日期", "2026-03-26（项目检索配置与原始导出记录日期）"],
        ["时间范围", "2020-2026；2026 年仅作为阶段性观察"],
        ["文献类型", "Article, Review, Conference Paper"],
        ["纳入标准", "与 LLM / generative AI 和 multi-agent / collaboration 主题同时相关"],
        ["排除标准", "重复记录、主题明显不相关或核心字段不可用记录"],
        ["去重规则", "优先 DOI 去重，随后按标题去重；542 条至 522 条"],
        ["工具版本", "Python 项目；pandas, networkx, matplotlib, Pillow 等依赖见 requirements.txt"],
        ["关键参数", "关键词共现阈值 >=2；作者合作展示阈值 >=2；高被引论文取 Top 10"],
    ]
    story.append(make_table(methods, [3.2 * cm, 12.1 * cm], style_sheet))
    story.append(Spacer(1, 5))

    story.append(p("2.2 研究问题与分析框架", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "根据课程要求，本文不把图表作为孤立展示，而是将每张图表绑定到可回答的研究问题。RQ1 关注该领域的发文增长与发展阶段；RQ2 关注研究主体与合作格局；RQ3 关注研究热点和主题结构；RQ4 关注高影响论文和知识基础；RQ5 在 Discussion 中综合前述证据讨论未来挑战。",
            "本文的分析流程包括：年度发文趋势分析、影响力指标分析、关键词共现分析、作者合作网络分析、高被引代表文献分析、共被引网络分析和参数敏感性分析。图表解释采用 Claim-Evidence-Reasoning 逻辑：先提出主张，再给出图表、指标或代表文献证据，最后说明证据如何支持结论以及其解释边界。",
        ],
        style_sheet["body"],
    )

    story.append(p("3. 文献计量结果", style_sheet["h1"]))
    story.append(p("3.1 年度发文趋势：2024-2025 年进入快速爆发期", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "年度发文量显示，LLM 多智能体协作研究具有明显的阶段性增长特征。2020 年仅 1 篇，2021 年 2 篇，2022 年 6 篇，2023 年 19 篇，2024 年增长至 81 篇，2025 年进一步达到 344 篇。2026 年已有 69 篇，但由于年份尚未结束，该数值不能与完整年份直接比较。该趋势支持的核心主张是：LLM 多智能体协作已经从概念探索转向快速扩张，但尚不能据此判断技术已经成熟。",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        REVIEW_FIG_DIR / "fig2_publication_growth_stages.png",
        "图 1 年度发文增长与发展阶段。数据来源为 Lens.org Scholarly Works，时间范围为 2020-2026 年，分析单位为文献记录，使用 Python 生成；纵轴为年度发文量，颜色区分早期探索、加速发展和爆发增长阶段。2026 年数据尚未覆盖全年，因此仅作为阶段性观察。",
        style_sheet,
        max_height=7.5 * cm,
    )

    story.append(p("3.2 作者合作网络：研究力量活跃但核心团队尚未高度稳定", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "作者合作网络用于回答“谁在研究这个领域，以及合作是否已经稳定”。项目统计显示，样本作者总数为 2,564，篇均作者数为 5.07。经过一次性合作过滤后，作者合作网络保留 51 个节点和 48 条边，说明当前研究虽参与者众多，但重复合作关系并不密集。该结果更适合解释为“研究力量正在扩张且合作结构仍然分散”，而不应简单转化为作者排名或机构排名。",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        FIG_DIR / "author_collaboration_network.png",
        "图 2 作者合作网络。数据来源为 Lens.org 2020-2026 年 522 篇清洗后文献，分析单位为作者；节点表示作者，连线表示同篇论文共同署名关系，展示阈值为合作次数至少 2 次，节点大小反映重复合作强度。该图用于回答 RQ2，即研究主体和合作格局是否已经形成稳定核心。",
        style_sheet,
        max_height=7.3 * cm,
    )

    story.append(p("3.3 关键词主题结构：从技术底座到垂直应用的四层框架", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "关键词统计显示，最高频关键词包括 artificial intelligence、large language models、machine learning、natural language processing、generative AI、agentic AI、multi-agent systems、retrieval-augmented generation、AI agents、human-robot interaction 和 digital health 等。这些关键词并非孤立出现，而是构成了一个由技术底座、协作架构、能力增强和应用治理组成的多层结构。",
            "图 3 将关键词共现结果转化为综述框架。第一层是 LLM/AI 技术底座，说明多智能体系统仍然依赖大模型本身的语言理解、生成和推理能力；第二层是智能体协作架构，关注角色分工、任务拆解、消息传递和多轮反思；第三层是 RAG/RL 等能力增强机制，解决知识更新、长期规划和反馈学习问题；第四层是治理与垂直应用，涵盖伦理、人机交互、数字健康、机器人和医疗等场景。",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        REVIEW_FIG_DIR / "fig3_thematic_architecture.png",
        "图 3 LLM 多智能体协作研究的主题架构。数据来源为 Lens.org 清洗后文献，时间范围为 2020-2026 年，分析单位为关键词；关键词在单篇文献内先去重，共现阈值为至少 2 次。图中层级表示从模型技术底座到协作架构、能力增强和应用治理的主题组织关系。",
        style_sheet,
        max_height=7.5 * cm,
    )

    story.append(p("3.4 高被引代表文献：从论文清单到知识基础", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "课程要求中的“1 表”应当支撑核心论述，而不是简单列出文献。本文按 Lens.org 的 Citing Works Count 排序，选择 Top 10 高被引论文作为 milestone 候选，并结合题名、来源和主题归属判断其在综述中的作用。表 1 显示，当前高影响文献主要分布在科学发现与自驱动实验室、机器人任务规划、人机协作和医疗智能体等方向。",
        ],
        style_sheet["body"],
    )
    top_rows = [["Rank", "Year", "Cites", "Theme", "Representative paper"]]
    for row in load_top_papers():
        top_rows.append([row["rank"], row["year"], row["citations"], row["theme"], short_title(row["title"], 72)])
    story.append(p("表 1 Top 10 高被引 milestone 候选论文。数据来源为 Lens.org 2020-2026 年清洗后文献；分析单位为单篇论文；排序指标为 Citing Works Count；筛选阈值为 Top 10。", style_sheet["caption"]))
    story.append(make_table(top_rows, [1.05 * cm, 1.25 * cm, 1.35 * cm, 3.15 * cm, 8.75 * cm], style_sheet))
    story.append(Spacer(1, 5))
    add_paragraphs(
        story,
        [
            "表 1 的解释边界也需要说明：被引次数高并不等于论文结论一定正确，也不等于技术路线已经成熟。高被引论文更适合作为知识基础和代表文献的线索，仍需要结合关键词主题、共被引关系和论文内容进行解释。本文因此把表 1 作为技术叙事的锚点，而不是把它当作简单排名。",
        ],
        style_sheet["body"],
    )

    add_figure(
        story,
        REVIEW_FIG_DIR / "fig6_reference_cocitation_network.png",
        "图 4 文献共被引网络。数据来源为 Lens.org 2020-2026 年清洗后语料，分析单位为被共同引用的代表性文献；节点大小表示语料内被引频次，连线表示共被引强度，颜色表示主题聚类。该图用于补充表 1，说明高被引论文背后的共同知识基础和主题簇。",
        style_sheet,
        max_height=7.8 * cm,
    )

    story.append(p("4. Discussion：技术叙事线、局限与未来议程", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "综合 RQ1-RQ4 的证据，LLM 多智能体协作研究可以归纳为四条技术叙事线。第一是多智能体任务规划与自动化工作流，代表性研究关注如何将自然语言目标转化为可执行计划，并在多个智能体之间分配任务。第二是科学发现与自驱动实验室，该方向强调将文献检索、假设生成、实验设计和结果分析连接为闭环科研流程。第三是人机协作与人类监督，它提醒我们多智能体系统并不只是多个 AI 的协作，更是人、模型、工具和环境之间的协作。第四是医疗、机器人和垂直行业应用，这些场景具有高约束、高风险和强专业性，对系统可靠性和可审计性提出更高要求。",
            "该领域的主要挑战也由图表证据和代表文献共同指向。首先，评价体系仍不统一，许多系统展示任务完成效果，却缺少可比较的 benchmark、失败恢复指标和成本指标。其次，协作机制仍缺乏可解释性：当多个智能体共同产生结果时，错误究竟来自检索、推理、通信还是工具调用，往往难以追踪。第三，垂直场景验证不足，医疗、机器人和科学实验等应用需要领域专家、真实约束和长期稳定性评估。第四，安全与伦理问题更加复杂，多智能体系统可能放大单模型风险，并引入权限边界、责任归属和审计机制等新问题。",
            "本文也存在局限。第一，数据仅来自 Lens.org，虽然覆盖 DOI、引用和开放获取等字段，但仍可能受到数据库收录和元数据质量影响。第二，2026 年数据尚未完整，因此趋势解释不能把 2026 年与完整年份直接比较。第三，References 字段覆盖率为 81.99%，足以进行初步共被引分析，但仍可能漏掉部分引用关系。第四，高被引 milestone 候选论文主要基于 Lens.org 被引次数排序，后续可结合突现检测、中介中心性、聚类位置和人工精读进一步增强判断。",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        REVIEW_FIG_DIR / "fig5_challenges_agenda.png",
        "图 5 挑战与未来研究议程。该图基于 RQ1-RQ4 的结果归纳未来研究方向，强调评价体系、协作机制、垂直场景验证和安全治理四类问题。图中箭头表示从当前瓶颈到后续研究议程的逻辑转化。",
        style_sheet,
        max_height=7.2 * cm,
    )

    story.append(p("5. 结论", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "本文基于 522 篇 Lens.org 文献，对 LLM 多智能体协作研究进行了文献计量型 mini review。研究发现，该领域在 2024-2025 年进入快速爆发期，研究主题已从单模型能力扩展到智能体协作架构、RAG/RL 能力增强、治理问题和垂直场景落地。作者合作网络说明研究力量仍处于扩张和分散阶段，高被引文献和共被引分析则帮助识别科学发现、机器人规划、人机协作和医疗智能体等知识基础。",
            "总体来看，LLM 多智能体协作的价值不在于简单增加智能体数量，而在于通过角色分工、证据检索、交叉检查和人类监督，将大语言模型嵌入更复杂、更可控的工作流。未来研究需要从演示型系统走向可评价、可解释、可审计和可落地的系统。只有当多智能体协作能够在真实约束下稳定运行，并清楚说明其证据、责任和边界时，它才可能从研究热点转化为可靠的智能基础设施。",
        ],
        style_sheet["body"],
    )

    story.append(p("AI 使用声明与项目材料", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "本课程项目允许 AI 辅助，但不允许编造引用、替代人工判断或生成无法核验的数据结论。本文写作过程中使用 AI 辅助进行结构整理、语言润色、图表解释逻辑检查和代码排查；所有核心数据、图表、文献表和结论均来自项目仓库中的可追溯文件，并经过人工核验。详细说明见 docs/ai_usage.md。",
            "主要项目材料包括：config/query.yaml、data/processed/cleaned_data.csv、outputs/metrics_summary.txt、outputs/keyword_statistics.txt、outputs/tables/top_cited_papers.md、outputs/figures/author_collaboration_network.png、outputs/review_figures/fig2_publication_growth_stages.png、outputs/review_figures/fig3_thematic_architecture.png、params.md 和 README.md。",
        ],
        style_sheet["body_no_indent"],
    )
    story.append(p("参考文献与项目材料", style_sheet["h1"]))
    for line in reference_lines("cn"):
        story.append(p(line, style_sheet["small"]))
    return story


def english_story(style_sheet):
    story = []
    story.append(p("A Bibliometric Mini Review of LLM-Based Multi-Agent Collaboration: Growth Dynamics, Knowledge Bases, and Future Agenda", style_sheet["title"]))
    story.append(p("Course Paper | A reproducible GitHub project based on 522 Lens.org records from 2020 to 2026", style_sheet["subtitle"]))
    story.append(p("Authors: Junjie Gao, Shiduo Zhao, Minghao Xie, Guangchen Yang, Bowei Luo", style_sheet["subtitle"]))
    story.append(Spacer(1, 6))

    story.append(p("Abstract", style_sheet["abstract_title"]))
    add_paragraphs(
        story,
        [
            "Large language models are increasingly moving beyond single-model question answering and text generation toward agentic systems that can decompose tasks, call tools, coordinate roles, and execute complex workflows. To clarify the intellectual structure and emerging trends of LLM-based multi-agent collaboration, this paper constructs a bibliometric dataset from Lens.org Scholarly Works covering 2020-2026. After DOI-based and title-based deduplication, 522 valid records were retained for analysis. We examine annual publication growth, citation impact, author collaboration, keyword co-occurrence, highly cited milestone candidates, and co-citation evidence, and then translate these bibliometric signals into a mini-review narrative.",
            "The results indicate that the field entered a rapid expansion stage in 2024-2025, with 344 publications in 2025. The corpus received 4,265 citations in total and reached an h-index of 31. The author collaboration network suggests an active but still fragmented research community, while keyword evidence points to a four-layer thematic architecture: LLM/AI foundations, agentic collaboration architectures, RAG/RL-based capability enhancement, and governance-oriented vertical applications. Combining the Top 10 highly cited papers with thematic interpretation, the review identifies four major storylines: scientific discovery and self-driving laboratories, robotic task planning, human-AI collaboration, and medical or vertical-domain agents. The paper concludes by discussing unresolved challenges in evaluation, explainability, real-world validation, and safety governance.",
        ],
        style_sheet["body_no_indent"],
    )
    story.append(p("Keywords: large language models; multi-agent systems; bibliometrics; keyword co-occurrence; co-citation network; mini review", style_sheet["note"]))

    story.append(p("1. Introduction", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "The development of large language models (LLMs) has reshaped the boundary of artificial intelligence systems. Early LLM applications mainly focused on question answering, summarization, translation, writing assistance, and code generation. With the rise of tool use, retrieval-augmented generation, long-context reasoning, and function calling, LLMs have increasingly been embedded into complex workflows where they can plan, retrieve, execute, evaluate, and revise.",
            "Compared with a single LLM, a multi-agent system is not merely a larger collection of models. Its central idea is to organize roles, communication, evidence retrieval, task decomposition, and cross-checking mechanisms so that complex tasks can be handled in a more structured way. In software engineering, different agents may handle requirement analysis, architecture design, coding, testing, and review. In scientific discovery, agents may support literature search, hypothesis generation, experiment design, data analysis, and report writing. In healthcare and robotics, LLM agents may serve as high-level planners or decision-support components, but they must also be constrained by domain expertise, safety boundaries, and human oversight.",
            "The field is expanding rapidly, which makes review writing difficult. New concepts, frameworks, and applications appear at high frequency, and the field spans artificial intelligence, robotics, software engineering, healthcare, chemistry, human-computer interaction, and safety governance. A purely narrative review may miss important structural signals. This paper therefore adopts a bibliometric mini-review approach: it uses reproducible data, figures, and representative papers to answer explicit research questions.",
        ],
        style_sheet["body"],
    )

    story.append(p("2. Data and Methods", style_sheet["h1"]))
    story.append(p("2.1 Data source, query strategy, and screening", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "The data were retrieved from Lens.org Scholarly Works. The search strategy follows an Object AND Method logic. The Object group includes Large Language Model*, LLM*, Generative AI, Foundation Model*, and ChatGPT, while the Method group includes Multi-agent*, Collaboration, Coordination, Cooperation, and Multi-agent system*. The time window was set to 2020-2026. Document types were limited to articles, reviews, and conference papers, and the language was limited to English. The query configuration is stored in config/query.yaml. The query log and the raw export file both indicate March 26, 2026 as the project record date, which is used here as the retrieval/export date.",
            "The initial Lens.org export contained 542 records. The dataset was deduplicated first by DOI and then by title, resulting in 522 valid records. In the cleaned dataset, Title and Publication Year have 100% coverage, Abstract has 98.28% coverage, References has 81.99% coverage, and DOI has 99.81% coverage. These fields support annual trend analysis, keyword co-occurrence, author collaboration, citation analysis, co-citation mapping, and milestone paper identification.",
        ],
        style_sheet["body"],
    )

    methods = [
        ["Transparency item", "Implementation in this paper"],
        ["Database", "Lens.org Scholarly Works"],
        ["Full query", "Object AND Method; see config/query.yaml"],
        ["Retrieval date", "2026-03-26, based on query log and raw export record"],
        ["Time window", "2020-2026; 2026 is treated as partial-year evidence"],
        ["Document types", "Article, Review, Conference Paper"],
        ["Inclusion criteria", "Records jointly related to LLM/generative AI and multi-agent/collaboration topics"],
        ["Exclusion criteria", "Duplicates, clearly irrelevant records, or unusable core metadata"],
        ["Deduplication", "DOI first, then title; 542 records reduced to 522"],
        ["Tools", "Python project using pandas, networkx, matplotlib, Pillow; dependencies in requirements.txt"],
        ["Key parameters", "Keyword co-occurrence threshold >=2; author-collaboration display threshold >=2; Top 10 highly cited papers"],
    ]
    story.append(make_table(methods, [3.2 * cm, 12.1 * cm], style_sheet))
    story.append(Spacer(1, 5))

    story.append(p("2.2 Research questions and analytical framework", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "Following the course requirement, figures are not treated as isolated visual outputs. Each figure or table is linked to a research question. RQ1 asks how the field has grown and which stage it has entered. RQ2 asks who participates in the field and whether stable collaboration groups have formed. RQ3 asks what the major research themes are and how they are structurally related. RQ4 asks which highly influential papers constitute the knowledge base. RQ5 synthesizes the evidence to discuss future challenges.",
            "The analysis includes annual publication trends, citation impact indicators, keyword co-occurrence, author collaboration, highly cited paper identification, co-citation analysis, and parameter sensitivity checks. The interpretation follows a Claim-Evidence-Reasoning logic: each main claim is supported by figures, indicators, or representative papers, and the reasoning explains both what can and cannot be inferred from the evidence.",
        ],
        style_sheet["body"],
    )

    story.append(p("3. Bibliometric Results", style_sheet["h1"]))
    story.append(p("3.1 Annual growth: rapid expansion after 2024", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "Annual publication counts reveal a clear stage transition. The dataset contains 1 paper in 2020, 2 in 2021, 6 in 2022, 19 in 2023, 81 in 2024, and 344 in 2025. The 2026 count is 69, but it should not be compared directly with complete calendar years. This pattern supports the claim that LLM-based multi-agent collaboration has moved from early conceptual exploration to rapid expansion, but it does not by itself prove that the technology is already mature.",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        REVIEW_FIG_DIR / "fig2_publication_growth_stages.png",
        "Figure 1. Annual publication growth and development stages. Data source: Lens.org Scholarly Works; time window: 2020-2026; unit of analysis: scholarly work; tool: Python. Bar height indicates annual publication count and color marks exploratory, accelerating, and explosive stages. The 2026 data are partial-year observations.",
        style_sheet,
        max_height=7.5 * cm,
    )

    story.append(p("3.2 Author collaboration: active participation but fragmented stable ties", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "The author collaboration network addresses who is working on this topic and whether stable collaboration groups have emerged. The corpus includes 2,564 authors, with an average of 5.07 authors per paper. After filtering one-off coauthorships, the displayed network contains 51 nodes and 48 edges. This suggests that the field is active and expanding, but repeated collaboration is not yet highly concentrated around a small number of core teams.",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        FIG_DIR / "author_collaboration_network.png",
        "Figure 2. Author collaboration network. Data source: 522 cleaned Lens.org records from 2020-2026; unit of analysis: author; edges represent coauthorship within the same paper; display threshold: at least two repeated collaborations. Node size reflects repeated collaboration strength. The figure answers RQ2 about collaboration structure.",
        style_sheet,
        max_height=7.3 * cm,
    )

    story.append(p("3.3 Keyword structure: a four-layer thematic architecture", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "The most frequent keywords include artificial intelligence, large language models, machine learning, natural language processing, generative AI, agentic AI, multi-agent systems, retrieval-augmented generation, AI agents, human-robot interaction, and digital health. These keywords form a layered structure rather than a random list of topics.",
            "Figure 3 translates the keyword evidence into a review framework. The first layer is the LLM/AI foundation, which provides language understanding, generation, reasoning, and knowledge representation. The second layer is the agentic collaboration architecture, involving role allocation, task decomposition, communication protocols, and reflection. The third layer includes RAG and reinforcement learning as capability-enhancement mechanisms. The fourth layer covers governance and vertical applications such as ethics, human-robot interaction, digital health, robotics, and medicine.",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        REVIEW_FIG_DIR / "fig3_thematic_architecture.png",
        "Figure 3. Thematic architecture of LLM-based multi-agent collaboration. Data source: cleaned Lens.org corpus, 2020-2026; unit of analysis: keyword; within-paper keywords are deduplicated; co-occurrence threshold: at least two occurrences. The layers summarize how technical foundations, collaboration architectures, capability enhancement, and applications are connected.",
        style_sheet,
        max_height=7.5 * cm,
    )

    story.append(p("3.4 Highly cited papers: from a paper list to a knowledge base", style_sheet["h2"]))
    add_paragraphs(
        story,
        [
            "The required table in a bibliometric review should support the argument rather than merely list papers. We rank papers by Lens.org Citing Works Count and select the Top 10 as first-pass milestone candidates. Table 1 indicates that influential works are concentrated around scientific discovery and self-driving laboratories, robotic task planning, human-AI collaboration, and medical or vertical-domain agents.",
        ],
        style_sheet["body"],
    )
    top_rows = [["Rank", "Year", "Cites", "Theme", "Representative paper"]]
    for row in load_top_papers():
        top_rows.append([row["rank"], row["year"], row["citations"], row["theme"], short_title(row["title"], 72)])
    story.append(p("Table 1. Top 10 highly cited milestone candidates. Data source: cleaned Lens.org records from 2020-2026; unit of analysis: paper; ranking metric: Citing Works Count; threshold: Top 10.", style_sheet["caption"]))
    story.append(make_table(top_rows, [1.05 * cm, 1.25 * cm, 1.35 * cm, 3.15 * cm, 8.75 * cm], style_sheet))
    story.append(Spacer(1, 5))
    add_paragraphs(
        story,
        [
            "Citation counts should be interpreted cautiously. A highly cited paper is not automatically correct, nor does it prove that a technical path has matured. It is better treated as an anchor for identifying knowledge bases and representative storylines. Therefore, this review uses Table 1 together with keyword and co-citation evidence rather than as a simple ranking.",
        ],
        style_sheet["body"],
    )

    add_figure(
        story,
        REVIEW_FIG_DIR / "fig6_reference_cocitation_network.png",
        "Figure 4. Reference co-citation network. Data source: cleaned Lens.org corpus from 2020-2026; unit of analysis: co-cited representative references. Node size indicates citation frequency within the corpus, edges indicate co-citation strength, and colors indicate thematic clusters. The figure complements Table 1 by showing shared knowledge bases behind highly cited papers.",
        style_sheet,
        max_height=7.8 * cm,
    )

    story.append(p("4. Discussion: storylines, limitations, and future agenda", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "The evidence supports four major storylines. The first is multi-agent task planning and automated workflows, where LLM agents transform natural-language goals into executable subtasks. The second is scientific discovery and self-driving laboratories, where agents can connect literature search, hypothesis generation, experiment design, and result analysis. The third is human-AI collaboration and human oversight, which reframes multi-agent systems as collaborations among humans, models, tools, and environments. The fourth is medical, robotic, and vertical-domain applications, where reliability, auditability, and domain constraints become essential.",
            "Several challenges remain. First, evaluation is not yet standardized: many systems demonstrate task completion but lack comparable benchmarks, failure-recovery metrics, and cost measures. Second, collaboration mechanisms remain difficult to explain; when a multi-agent system fails, it is often unclear whether the error comes from retrieval, reasoning, communication, or tool execution. Third, vertical scenarios require stronger real-world validation by domain experts. Fourth, safety and ethical issues are more complex in multi-agent settings because multiple agents may amplify each other's errors or blur responsibility boundaries.",
            "This review has limitations. It uses Lens.org as the sole database, so the results may be influenced by database coverage and metadata quality. The 2026 data are incomplete and should not be compared directly with full years. References coverage is 81.99%, which supports an initial co-citation analysis but may miss some citation relations. Finally, the milestone candidates are based primarily on Lens.org citation counts; future work can integrate burst detection, betweenness centrality, cluster position, and manual full-text reading.",
        ],
        style_sheet["body"],
    )
    add_figure(
        story,
        REVIEW_FIG_DIR / "fig5_challenges_agenda.png",
        "Figure 5. Challenges and future research agenda. This figure synthesizes RQ1-RQ4 into four future directions: evaluation, collaboration mechanisms, vertical-scenario validation, and safety governance. Arrows indicate how current bottlenecks are translated into research agenda items.",
        style_sheet,
        max_height=7.2 * cm,
    )

    story.append(p("5. Conclusion", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "Based on 522 Lens.org records, this paper provides a bibliometric mini review of LLM-based multi-agent collaboration. The field entered rapid expansion in 2024-2025, and its thematic structure has moved beyond single-model capability toward agentic collaboration architectures, RAG/RL-based enhancement, governance issues, and vertical applications. The author collaboration network suggests an expanding but still fragmented community, while highly cited papers and co-citation evidence help identify scientific discovery, robotic planning, human-AI collaboration, and medical agents as major knowledge bases.",
            "The value of LLM-based multi-agent collaboration is not simply the addition of more agents. Its value lies in embedding LLMs into more controllable workflows through role division, evidence retrieval, cross-checking, and human oversight. Future research should move from demonstration systems toward systems that are evaluable, explainable, auditable, and deployable under real constraints.",
        ],
        style_sheet["body"],
    )

    story.append(p("AI Use Statement and Project Materials", style_sheet["h1"]))
    add_paragraphs(
        story,
        [
            "AI assistance was used for structure checking, language polishing, figure-interpretation logic, and code troubleshooting. It was not used to fabricate references, replace human judgment, or generate unverifiable data conclusions. All core data, figures, tables, and claims are traceable to the GitHub project and were manually checked. The detailed statement is stored in docs/ai_usage.md.",
            "Key project materials include config/query.yaml, data/processed/cleaned_data.csv, outputs/metrics_summary.txt, outputs/keyword_statistics.txt, outputs/tables/top_cited_papers.md, outputs/figures/author_collaboration_network.png, outputs/review_figures/fig2_publication_growth_stages.png, outputs/review_figures/fig3_thematic_architecture.png, params.md, and README.md.",
        ],
        style_sheet["body_no_indent"],
    )
    story.append(p("References and Project Materials", style_sheet["h1"]))
    for line in reference_lines("en"):
        story.append(p(line, style_sheet["small"]))
    return story


def build_pdf(filename: str, story, running_title: str):
    doc = SimpleDocTemplate(
        str(PAPER_DIR / filename),
        pagesize=A4,
        leftMargin=1.75 * cm,
        rightMargin=1.75 * cm,
        topMargin=1.55 * cm,
        bottomMargin=1.75 * cm,
        title=filename,
        author="LLM Trends Analysis Course Project",
    )
    decorator = page_decorator(running_title)
    doc.build(story, onFirstPage=decorator, onLaterPages=decorator)


def main():
    register_fonts()
    style_sheet = styles()
    build_pdf("course_paper_cn.pdf", chinese_story(style_sheet), "文献计量学课程论文｜LLM 多智能体协作")
    build_pdf("course_paper_en.pdf", english_story(style_sheet), "Bibliometrics Course Paper | LLM Multi-Agent Collaboration")
    print(PAPER_DIR / "course_paper_cn.pdf")
    print(PAPER_DIR / "course_paper_en.pdf")


if __name__ == "__main__":
    main()
