import math
import os
import textwrap
from collections import Counter

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


OUT_DIR = os.path.join("outputs", "review_figures")
WIDTH = 2200
HEIGHT = 1400
BG = "#FAF9F5"
BG_COOL = "#F5F8FB"
BG_WHITE = "#FFFFFF"
BG_WARM = "#FBF7EF"
BG_DARK = "#F6F4F8"
INK = "#26323B"
MUTED = "#667682"
GRID = "#DADDD6"
BLUE = "#2F6F9F"
TEAL = "#3B9C8A"
GOLD = "#C99A2E"
CORAL = "#D66A4A"
PLUM = "#8B5A8C"
GREEN = "#5A8F55"
PALE_BLUE = "#E5F0F6"
PALE_TEAL = "#E4F2EE"
PALE_GOLD = "#F4E9CA"
PALE_CORAL = "#F6DDD4"
PALE_PLUM = "#EFE3F0"


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(os.path.join("C:\\Windows\\Fonts", name), size)


F_TITLE = font(58, True)
F_SUB = font(30)
F_H1 = font(34, True)
F_H2 = font(28, True)
F_TEXT = font(25)
F_SMALL = font(21)
F_TINY = font(18)


def new_canvas(title, subtitle, bg=BG):
    img = Image.new("RGB", (WIDTH, HEIGHT), bg)
    d = ImageDraw.Draw(img)
    d.text((95, 70), title, fill=INK, font=F_TITLE)
    d.text((98, 150), subtitle, fill=MUTED, font=F_SUB)
    d.line((95, 205, WIDTH - 95, 205), fill=GRID, width=3)
    return img, d


def rounded(d, box, fill, outline="#DFDAD2", radius=22, width=2):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_width(d, text, fnt):
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def draw_wrapped(d, text, x, y, max_width, fnt=F_SMALL, fill=MUTED, gap=6, max_lines=None):
    lines = []
    for para in str(text).split("\n"):
        words = para.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if text_width(d, trial, fnt) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + gap
    return y


def arrow(d, start, end, fill="#C2C8C8", width=5):
    x1, y1 = start
    x2, y2 = end
    d.line((x1, y1, x2, y2), fill=fill, width=width)
    if x2 >= x1:
        pts = [(x2, y2), (x2 - 20, y2 - 11), (x2 - 20, y2 + 11)]
    else:
        pts = [(x2, y2), (x2 + 20, y2 - 11), (x2 + 20, y2 + 11)]
    d.polygon(pts, fill=fill)


def save(img, filename):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)
    img.save(path, quality=95)
    print(path)


def load_df():
    df = pd.read_csv("data/processed/cleaned_data.csv")
    df.columns = df.columns.str.strip()
    return df


def make_fig1_methodology():
    img, d = new_canvas(
        "Fig. 1. Literature Retrieval and Review Design",
        "A reproducible bibliometric workflow adapted for the LLM multi-agent collaboration review",
        BG_COOL,
    )

    steps = [
        ("Search Design", "(Object) AND (Method)\nLLM / Generative AI + Multi-agent / Collaboration", BLUE),
        ("Lens.org Export", "542 scholarly records\n2020-2026, Article / Review / Conference Paper", TEAL),
        ("Data Cleaning", "DOI + Title de-duplication\n522 valid records retained", GOLD),
        ("Bibliometric Mapping", "Trend, citation impact,\nkeyword co-occurrence, collaboration", CORAL),
        ("Review Synthesis", "Technical narratives,\nchallenges, and future agenda", PLUM),
    ]
    x, y, w, h, gap = 95, 310, 365, 230, 55
    centers = []
    for title, body, color in steps:
        rounded(d, (x, y, x + w, y + h), "#FFFFFF", outline="#C9D5DD")
        d.rectangle((x, y, x + w, y + 18), fill=color)
        d.text((x + 28, y + 48), title, fill=color, font=F_H1)
        draw_wrapped(d, body, x + 28, y + 100, w - 56, F_SMALL, MUTED)
        centers.append((x + w, y + h // 2))
        x += w + gap
    for i in range(len(centers) - 1):
        arrow(d, (centers[i][0] + 5, centers[i][1]), (centers[i + 1][0] - w - 10, centers[i + 1][1]))

    rounded(d, (160, 720, 645, 1030), "#DFECF5", outline=None)
    rounded(d, (705, 720, 1190, 1030), "#E8F1F7", outline=None)
    rounded(d, (1250, 720, 1735, 1030), "#F4F0E6", outline=None)
    rounded(d, (1795, 720, 2105, 1030), "#EFE7F1", outline=None)

    panels = [
        (160, "Transparency", "Database, search string, year window, document type, cleaning rules, and parameters are explicitly recorded."),
        (705, "Evidence", "Bibliometric maps decide what to discuss: growth stages, themes, actors, and milestone candidates."),
        (1250, "Narrative", "Clusters are translated into technical storylines: planning, scientific discovery, human-AI teaming, and vertical agents."),
        (1795, "Output", "A compact review with figures, discussion, limitations, and future directions."),
    ]
    for px, head, body in panels:
        d.text((px + 28, 760), head, fill=INK, font=F_H1)
        draw_wrapped(d, body, px + 28, 820, 420 if px < 1795 else 250, F_SMALL, MUTED)

    d.text((95, 1240), "Caption: The review follows a transparent bibliometric workflow: search and cleaning define the corpus, mapping identifies evidence, and synthesis converts evidence into review sections.", fill=MUTED, font=F_SMALL)
    save(img, "fig1_methodology_workflow.png")


def make_fig2_trend(df):
    img, d = new_canvas(
        "Fig. 2. Publication Growth and Development Stages",
        "Annual output of LLM multi-agent collaboration research, 2020-2026",
        BG_WHITE,
    )
    counts = df["Publication Year"].value_counts().sort_index().to_dict()
    years = list(range(2020, 2027))
    values = [int(counts.get(y, 0)) for y in years]
    max_v = max(values)

    plot = (180, 320, 1980, 1040)
    x0, y0, x1, y1 = plot
    d.line((x0, y1, x1, y1), fill=INK, width=3)
    d.line((x0, y0, x0, y1), fill=INK, width=3)
    for t in [0, 100, 200, 300, 400]:
        yy = y1 - int((t / 400) * (y1 - y0))
        d.line((x0, yy, x1, yy), fill="#E5E4DD", width=2)
        d.text((105, yy - 13), str(t), fill=MUTED, font=F_TINY)

    bar_gap = 36
    bar_w = int((x1 - x0 - bar_gap * (len(years) + 1)) / len(years))
    points = []
    for i, (year, val) in enumerate(zip(years, values)):
        bx = x0 + bar_gap + i * (bar_w + bar_gap)
        bh = int((val / 400) * (y1 - y0))
        color = "#6B8FB3" if year <= 2023 else ("#E0A72E" if year == 2024 else "#D84A38" if year == 2025 else "#7B6AA8")
        d.rounded_rectangle((bx, y1 - bh, bx + bar_w, y1), radius=10, fill=color)
        d.text((bx + bar_w // 2, y1 + 24), str(year), fill=INK, font=F_SMALL, anchor="mm")
        d.text((bx + bar_w // 2, y1 - bh - 30), str(val), fill=INK, font=F_H2, anchor="mm")
        points.append((bx + bar_w // 2, y1 - bh))

    for a, b in zip(points, points[1:]):
        d.line((a[0], a[1], b[0], b[1]), fill="#333333", width=4)
        d.ellipse((a[0] - 8, a[1] - 8, a[0] + 8, a[1] + 8), fill="#333333")
    last = points[-1]
    d.ellipse((last[0] - 8, last[1] - 8, last[0] + 8, last[1] + 8), fill="#333333")

    stage_boxes = [
        (230, 255, 650, 305, "Emergence: scattered early studies", BLUE),
        (820, 255, 1220, 305, "Acceleration: agentic AI appears", GOLD),
        (1390, 255, 1870, 305, "Explosion: workflow and vertical agents", CORAL),
    ]
    for a, b, c, e, label, color in stage_boxes:
        rounded(d, (a, b, c, e), "#FFFFFF", outline=color, radius=12, width=3)
        d.text((a + 18, b + 13), label, fill=color, font=F_SMALL)

    d.text((95, 1240), "Caption: Publication output rises sharply after 2024, indicating a transition from early exploration to high-intensity expansion. The 2026 bar is incomplete and should not be compared with full years.", fill=MUTED, font=F_SMALL)
    save(img, "fig2_publication_growth_stages.png")


def make_fig3_theme_architecture():
    img, d = new_canvas(
        "Fig. 3. Thematic Architecture of LLM Multi-Agent Collaboration",
        "A four-layer synthesis derived from keyword co-occurrence and milestone-paper interpretation",
        BG_DARK,
    )
    cx, cy = WIDTH // 2, 710
    layers = [
        (520, "#E8EEF8", "#4D6FA8", "LLM / AI Foundation", "large language models, artificial intelligence, machine learning, NLP"),
        (420, "#E4F2EA", "#3C8C66", "Agentic Architecture", "agentic AI, multi-agent systems, role assignment, communication"),
        (315, "#F7EBCB", "#C18D16", "Capability Enhancement", "RAG, reinforcement learning, planning, workflow optimization"),
        (205, "#F7DED7", "#C95E45", "Governance and Applications", "ethics, human-robot interaction, digital health, clinical agents"),
    ]
    for r, fill, outline, title, body in layers:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=5)
    labels = [
        (cx - 870, cy - 345, layers[0]),
        (cx + 560, cy - 340, layers[1]),
        (cx - 870, cy + 165, layers[2]),
        (cx + 560, cy + 175, layers[3]),
    ]
    anchor_points = [(cx - 390, cy - 260), (cx + 330, cy - 260), (cx - 300, cy + 255), (cx + 205, cy + 185)]
    for (lx, ly, (_, _, color, title, body)), ap in zip(labels, anchor_points):
        rounded(d, (lx, ly, lx + 520, ly + 185), "#FFFFFF", outline=color, radius=16, width=3)
        d.text((lx + 25, ly + 24), title, fill=color, font=F_H2)
        draw_wrapped(d, body, lx + 25, ly + 72, 455, F_SMALL, MUTED)
        d.line((lx + 260, ly + 185 if ly < cy else ly, ap[0], ap[1]), fill=color, width=3)
    d.text((cx, cy - 26), "LLM\nMulti-Agent\nCollaboration", fill=INK, font=F_H1, anchor="mm", align="center")
    d.text((95, 1240), "Caption: The topic structure can be read as nested layers: LLM capabilities support agentic architectures; RAG/RL enhances these agents; applications and governance define practical boundaries.", fill=MUTED, font=F_SMALL)
    save(img, "fig3_thematic_architecture.png")


def make_fig4_milestone_roadmap(df):
    img, d = new_canvas(
        "Fig. 4. Milestone Candidate Matrix",
        "Top-cited papers are grouped into technical narratives rather than treated as isolated rankings",
        BG_WARM,
    )
    top = df[["Title", "Publication Year", "Citing Works Count", "Source Title"]].copy()
    top["Citing Works Count"] = pd.to_numeric(top["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    top = top.sort_values(["Citing Works Count", "Publication Year"], ascending=[False, True]).head(10)
    short_labels = {
        0: "Self-driving labs",
        1: "UAV review",
        2: "Co-writing with LMs",
        3: "Chemistry agents review",
        4: "SMART-LLM",
        5: "Clinical agents",
        6: "Human-AI teaming",
        7: "RoCo robots",
        8: "LLM-HRI",
        9: "Radiology AI guide",
    }
    groups = [
        ("Scientific discovery", [0, 3], "#007A78", "#DDF2EF"),
        ("Robotics and planning", [4, 7], "#C44E52", "#F5DFDD"),
        ("Human-AI teaming", [2, 6, 8], "#8A6F00", "#F3E8BA"),
        ("Clinical / medical agents", [5, 9], "#6F579B", "#EAE3F3"),
    ]
    left = 105
    top_y = 300
    row_h = 230
    label_w = 385
    card_w = 760
    gap = 32
    max_cite = int(top["Citing Works Count"].max())

    d.text((left + label_w + 35, 250), "Representative high-impact candidates", fill=INK, font=F_H2)
    d.text((left + label_w + card_w + gap + 55, 250), "Review interpretation", fill=INK, font=F_H2)

    interpretations = {
        "Scientific discovery": "LLM agents are used to connect literature, hypothesis generation, experiment planning, and analysis loops.",
        "Robotics and planning": "Natural-language goals are converted into executable multi-robot or multi-step plans.",
        "Human-AI teaming": "The field expands from autonomous agents to collaborative systems involving human oversight and shared work.",
        "Clinical / medical agents": "High-risk domains require evidence grounding, expert review, and constrained deployment.",
    }

    for r, (label, idxs, color, pale) in enumerate(groups):
        y = top_y + r * row_h
        rounded(d, (left, y, WIDTH - 105, y + row_h - 24), "#FFFFFF", "#DDD8CF", radius=18, width=2)
        d.rectangle((left, y, left + 18, y + row_h - 24), fill=color)
        d.text((left + 42, y + 35), label, fill=color, font=F_H2)
        d.text((left + 42, y + 82), f"{len(idxs)} milestone candidates", fill=MUTED, font=F_SMALL)

        cy = y + 113
        x = left + label_w + 35
        for idx in idxs:
            row = top.iloc[idx]
            cite = int(row["Citing Works Count"])
            radius = int(24 + 30 * math.sqrt(cite / max_cite))
            d.ellipse((x, cy - radius, x + radius * 2, cy + radius), fill=color, outline="white", width=4)
            d.text((x + radius, cy - 7), str(cite), fill="white", font=F_TINY, anchor="mm")
            d.text((x + radius * 2 + 16, cy - 34), f"#{idx + 1} | {int(row['Publication Year'])}", fill=color, font=F_TINY)
            d.text((x + radius * 2 + 16, cy - 6), short_labels.get(idx, "Milestone candidate"), fill=INK, font=F_TINY)
            x += 270 if len(idxs) > 2 else 430

        ix = left + label_w + card_w + gap + 40
        rounded(d, (ix, y + 38, WIDTH - 150, y + row_h - 62), pale, outline=None, radius=16, width=0)
        draw_wrapped(d, interpretations[label], ix + 28, y + 72, 560, F_SMALL, INK, gap=7)

    d.text((95, 1240), "Caption: Bubble size encodes Lens.org citing works count. The matrix links highly cited candidate papers to the four technical narratives used in the review.", fill=MUTED, font=F_SMALL)
    save(img, "fig4_milestone_roadmap.png")


def make_fig5_challenges():
    img, d = new_canvas(
        "Fig. 5. Challenges and Future Research Agenda",
        "From demonstration systems to reliable, auditable, and domain-grounded multi-agent infrastructure",
        "#F8F8F8",
    )
    items = [
        ("Evaluation", "Heterogeneous tasks, metrics, prompts and tool settings make systems difficult to compare.", "Build shared benchmarks that report success, robustness, cost, safety and human effort.", "#276FBF"),
        ("Explainability", "Agent interactions often remain opaque; errors are hard to trace across the collaboration chain.", "Record role decisions, communication logs, tool calls, evidence paths and failure recovery.", "#2A9D8F"),
        ("Vertical validation", "Medical, robotic and scientific applications require domain constraints beyond general chat success.", "Integrate guidelines, expert review, structured outputs, permissions and rollback mechanisms.", "#E9A227"),
        ("Safety governance", "Multi-agent systems can amplify errors or blur responsibility when tools and agents interact.", "Define communication protocols, accountability boundaries, audit trails and human oversight.", "#D1495B"),
    ]
    y = 300
    for title, problem, future, color in items:
        rounded(d, (130, y, 2050, y + 210), "#FFFFFF", outline="#DDD8CF", radius=18, width=2)
        d.rectangle((130, y, 150, y + 210), fill=color)
        d.text((180, y + 28), title, fill=color, font=F_H1)
        d.text((520, y + 28), "Current bottleneck", fill=INK, font=F_H2)
        d.text((1260, y + 28), "Future direction", fill=INK, font=F_H2)
        draw_wrapped(d, problem, 520, y + 76, 610, F_SMALL, MUTED)
        draw_wrapped(d, future, 1260, y + 76, 650, F_SMALL, MUTED)
        arrow(d, (1160, y + 115), (1230, y + 115), color, 5)
        y += 240
    d.text((95, 1240), "Caption: The next phase of LLM multi-agent research requires moving beyond impressive demonstrations toward comparable evaluation, interpretable collaboration, domain validation, and safety governance.", fill=MUTED, font=F_SMALL)
    save(img, "fig5_challenges_agenda.png")


def main():
    df = load_df()
    make_fig1_methodology()
    make_fig2_trend(df)
    make_fig3_theme_architecture()
    make_fig4_milestone_roadmap(df)
    make_fig5_challenges()


if __name__ == "__main__":
    main()
