import math
import os
import textwrap
from collections import Counter, defaultdict

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


WIDTH = 1800
HEIGHT = 1200
BG = "#F8F7F2"
INK = "#24313B"
MUTED = "#687782"
GRID = "#D9DDD7"
BLUE = "#2F6F9F"
TEAL = "#3B9C8A"
GOLD = "#C99A2E"
CORAL = "#D66A4A"
PLUM = "#8B5A8C"
GREEN = "#5A8F55"
LIGHT_BLUE = "#DCEBF2"
LIGHT_TEAL = "#DDEFEA"
LIGHT_GOLD = "#F2E8C9"
LIGHT_CORAL = "#F5DDD5"


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = os.path.join("C:\\Windows\\Fonts", name)
    return ImageFont.truetype(path, size=size)


F_TITLE = font(52, True)
F_SUBTITLE = font(27)
F_LABEL = font(25, True)
F_TEXT = font(24)
F_SMALL = font(21)
F_TINY = font(18)


def load_data():
    df = pd.read_csv("data/processed/cleaned_data.csv")
    df.columns = df.columns.str.strip()
    return df


def canvas(title, subtitle):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.text((90, 58), title, fill=INK, font=F_TITLE)
    draw.text((92, 128), subtitle, fill=MUTED, font=F_SUBTITLE)
    draw.line((90, 178, WIDTH - 90, 178), fill=GRID, width=3)
    return img, draw


def save(img, filename):
    path = os.path.join("outputs", "figures", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, quality=95)
    print(f"saved {path}")


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_wrapped(draw, xy, text, fnt, fill, width, line_gap=7):
    x, y = xy
    lines = []
    for para in str(text).split("\n"):
        words = para.split()
        line = ""
        for word in words:
            test = (line + " " + word).strip()
            if text_size(draw, test, fnt)[0] <= width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    for line in lines:
        draw.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + line_gap
    return y


def rounded_rect(draw, box, fill, outline=None, width=1, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def normalize_keywords(raw):
    if pd.isna(raw):
        return []
    seen = set()
    out = []
    for kw in str(raw).split(";"):
        clean = " ".join(kw.strip().lower().split())
        if len(clean) <= 2 or clean in seen:
            continue
        seen.add(clean)
        out.append(clean)
    return out


def split_authors(raw):
    if pd.isna(raw):
        return []
    invalid = {"", "null", "null null", "nan", "none", "unknown"}
    out = []
    for name in str(raw).split(";"):
        clean = " ".join(name.strip().split())
        if clean.lower() not in invalid:
            out.append(clean)
    return out


def draw_keyword_cooccurrence(df):
    img, draw = canvas(
        "Keyword Co-occurrence Map",
        "LLM multi-agent research clusters, based on 522 Lens.org records",
    )

    keyword_counts = Counter()
    pair_counts = Counter()
    for _, row in df.iterrows():
        kws = normalize_keywords(row.get("Keywords"))
        keyword_counts.update(kws)
        for i, a in enumerate(kws):
            for b in kws[i + 1 :]:
                pair_counts[tuple(sorted((a, b)))] += 1

    selected = [
        "artificial intelligence",
        "large language models",
        "large language model",
        "generative ai",
        "agentic ai",
        "multi-agent systems",
        "ai agents",
        "retrieval-augmented generation",
        "reinforcement learning",
        "natural language processing",
        "machine learning",
        "deep learning",
        "ethics",
        "chatgpt",
        "human-robot interaction",
        "digital health",
    ]
    selected = [kw for kw in selected if kw in keyword_counts]

    positions = {
        "artificial intelligence": (860, 555),
        "large language models": (585, 420),
        "large language model": (545, 635),
        "machine learning": (830, 340),
        "natural language processing": (1015, 380),
        "deep learning": (1030, 590),
        "generative ai": (740, 720),
        "agentic ai": (1210, 520),
        "multi-agent systems": (1320, 665),
        "ai agents": (1270, 360),
        "retrieval-augmented generation": (1090, 765),
        "reinforcement learning": (730, 820),
        "ethics": (405, 760),
        "chatgpt": (365, 575),
        "human-robot interaction": (1370, 815),
        "digital health": (500, 875),
    }
    colors = {
        "artificial intelligence": BLUE,
        "large language models": BLUE,
        "large language model": BLUE,
        "machine learning": TEAL,
        "natural language processing": TEAL,
        "deep learning": TEAL,
        "generative ai": GOLD,
        "agentic ai": GOLD,
        "multi-agent systems": CORAL,
        "ai agents": CORAL,
        "retrieval-augmented generation": PLUM,
        "reinforcement learning": PLUM,
        "ethics": GREEN,
        "chatgpt": GREEN,
        "human-robot interaction": CORAL,
        "digital health": GREEN,
    }

    max_pair = max([v for k, v in pair_counts.items() if k[0] in selected and k[1] in selected] or [1])
    for (a, b), count in pair_counts.most_common(80):
        if a not in positions or b not in positions or count < 2:
            continue
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        width = max(2, int(2 + 10 * count / max_pair))
        draw.line((x1, y1, x2, y2), fill="#BFC8C8", width=width)

    max_count = max(keyword_counts[kw] for kw in selected)
    for kw in selected:
        x, y = positions[kw]
        count = keyword_counts[kw]
        r = int(34 + 60 * math.sqrt(count / max_count))
        fill = colors.get(kw, BLUE)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline="white", width=5)
        draw.text((x, y - 12), str(count), fill="white", font=F_LABEL, anchor="mm")

        label = kw.replace("large language models", "LLMs").replace("large language model", "LLM")
        lines = textwrap.wrap(label.title(), width=18)
        yy = y + r + 12
        for line in lines[:2]:
            draw.text((x, yy), line, fill=INK, font=F_SMALL, anchor="ma")
            yy += 24

    legend = [
        (BLUE, "LLM / AI foundation"),
        (CORAL, "Agent collaboration"),
        (PLUM, "Capability enhancement"),
        (GREEN, "Governance and applications"),
    ]
    lx, ly = 90, 1010
    for color, label in legend:
        draw.ellipse((lx, ly, lx + 26, ly + 26), fill=color)
        draw.text((lx + 40, ly - 1), label, fill=INK, font=F_SMALL)
        lx += 365

    draw.text((90, 1080), "Node size = keyword frequency; edge width = co-occurrence strength. Duplicated keywords within one paper are de-duplicated.", fill=MUTED, font=F_SMALL)
    save(img, "keyword_cooccurrence_network.png")


def draw_author_collaboration(df):
    img, draw = canvas(
        "Author Collaboration Network",
        "Core repeated collaborations after filtering one-off coauthorships",
    )

    pair_counts = Counter()
    author_counts = Counter()
    for _, row in df.iterrows():
        authors = split_authors(row.get("Author/s"))
        author_counts.update(authors)
        for i, a in enumerate(authors):
            for b in authors[i + 1 :]:
                pair_counts[tuple(sorted((a, b)))] += 1

    edges = [(a, b, c) for (a, b), c in pair_counts.items() if c >= 2]
    nodes = Counter()
    for a, b, c in edges:
        nodes[a] += c
        nodes[b] += c
    top_nodes = [name for name, _ in nodes.most_common(42)]
    edges = [(a, b, c) for a, b, c in edges if a in top_nodes and b in top_nodes]

    groups = []
    seen = set()
    adjacency = defaultdict(set)
    for a, b, _ in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    for node in top_nodes:
        if node in seen:
            continue
        stack = [node]
        comp = []
        seen.add(node)
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nb in adjacency[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        groups.append(comp)
    groups = sorted(groups, key=len, reverse=True)[:7]

    centers = [(410, 430), (880, 405), (1285, 430), (520, 805), (1000, 805), (1390, 805), (250, 760)]
    palette = [BLUE, CORAL, TEAL, GOLD, PLUM, GREEN, "#7C6F64"]

    pos = {}
    for gi, group in enumerate(groups):
        cx, cy = centers[gi]
        radius = 120 if len(group) > 4 else 80
        for i, name in enumerate(group):
            angle = 2 * math.pi * i / max(len(group), 1)
            pos[name] = (cx + int(radius * math.cos(angle)), cy + int(radius * math.sin(angle)))
        draw.ellipse((cx - radius - 62, cy - radius - 62, cx + radius + 62, cy + radius + 62), outline="#E1E2DC", width=3)
        draw.text((cx, cy - radius - 95), f"Component {gi + 1}", fill=palette[gi], font=F_LABEL, anchor="ma")

    max_edge = max([c for _, _, c in edges] or [1])
    for a, b, c in edges:
        if a not in pos or b not in pos:
            continue
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        draw.line((x1, y1, x2, y2), fill="#BBC7CC", width=max(2, int(2 + 7 * c / max_edge)))

    max_node = max([nodes[n] for n in pos] or [1])
    for name, (x, y) in pos.items():
        r = int(20 + 22 * nodes[name] / max_node)
        color = palette[min(next((i for i, g in enumerate(groups) if name in g), 0), len(palette) - 1)]
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline="white", width=4)
        if nodes[name] >= 3 or author_counts[name] >= 2:
            label = name if len(name) <= 22 else name[:21] + "."
            draw.text((x, y + r + 8), label, fill=INK, font=F_TINY, anchor="ma")

    panel = (1120, 220, 1685, 355)
    rounded_rect(draw, panel, "#FFFFFF", "#E4E1D9", 2, 16)
    draw.text((1145, 242), "Network reading", fill=INK, font=F_LABEL)
    draw.text((1145, 285), "Only collaborations repeated at least twice are shown.", fill=MUTED, font=F_SMALL)
    draw.text((1145, 318), "Result: fragmented teams, no dominant hub yet.", fill=MUTED, font=F_SMALL)

    draw.text((90, 1080), "Node size = repeated collaboration strength; components show stable coauthor groups. One-off collaborations are omitted for readability.", fill=MUTED, font=F_SMALL)
    save(img, "author_collaboration_network.png")


def draw_country_distribution(df):
    img, draw = canvas(
        "Institution / Country Distribution",
        "Geographic concentration of publication sources in the LLM multi-agent dataset",
    )

    counts = Counter()
    for country in df["Source Country"].dropna().astype(str):
        clean = country.strip()
        if clean and clean.lower() != "nan":
            counts[clean] += 1
    top = counts.most_common(14)
    max_count = max(c for _, c in top)

    x0, y0 = 250, 250
    bar_w = 1100
    row_h = 55
    for i, (country, count) in enumerate(top):
        y = y0 + i * row_h
        draw.text((90, y + 8), country, fill=INK, font=F_TEXT)
        draw.line((x0, y + 28, x0 + bar_w, y + 28), fill="#E6E5DF", width=14)
        fill_w = int(bar_w * count / max_count)
        color = [BLUE, TEAL, GOLD, CORAL, PLUM, GREEN][i % 6]
        draw.line((x0, y + 28, x0 + fill_w, y + 28), fill=color, width=18)
        draw.text((x0 + fill_w + 18, y + 11), str(count), fill=INK, font=F_LABEL)

    total_known = sum(counts.values())
    unknown = len(df) - total_known
    cards = [
        ("Known country records", total_known, LIGHT_BLUE, BLUE),
        ("Missing country field", unknown, LIGHT_CORAL, CORAL),
        ("Countries / regions", len(counts), LIGHT_TEAL, TEAL),
    ]
    cx = 1180
    for i, (label, value, bg, color) in enumerate(cards):
        y = 805 + i * 95
        rounded_rect(draw, (cx, y, 1660, y + 72), bg, None, radius=14)
        draw.text((cx + 24, y + 14), label, fill=MUTED, font=F_SMALL)
        draw.text((cx + 390, y + 13), str(value), fill=color, font=font(34, True), anchor="ra")

    draw.text((90, 1080), "Bars show source-country counts from Lens.org metadata. Missing country metadata is reported separately instead of being hidden.", fill=MUTED, font=F_SMALL)
    save(img, "institution_country_network.png")


def draw_citation_network(df):
    img, draw = canvas(
        "Milestone Paper Influence Map",
        "Top cited candidate papers used as first-pass knowledge anchors",
    )

    cols = ["Title", "Publication Year", "Citing Works Count", "Source Title", "DOI"]
    top = df[cols].copy()
    top["Citing Works Count"] = pd.to_numeric(top["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    top = top.sort_values(["Citing Works Count", "Publication Year"], ascending=[False, True]).head(10)
    max_cite = int(top["Citing Works Count"].max())

    x0, y0 = 100, 232
    bar_x = 720
    bar_w = 775
    row_h = 79
    palette = [BLUE, CORAL, TEAL, GOLD, PLUM, GREEN, "#7C6F64", "#4B778D", "#B56A7A", "#8A9A5B"]

    for idx, (_, row) in enumerate(top.iterrows()):
        y = y0 + idx * row_h
        year = int(row["Publication Year"])
        cite = int(row["Citing Works Count"])
        title = str(row["Title"])
        source = str(row["Source Title"])
        color = palette[idx]

        draw.text((x0, y), f"#{idx + 1}", fill=color, font=F_LABEL)
        draw.text((x0 + 62, y), str(year), fill=MUTED, font=F_SMALL)
        title_lines = textwrap.wrap(title, width=52)[:2]
        for j, line in enumerate(title_lines):
            draw.text((x0 + 150, y - 3 + j * 22), line, fill=INK, font=F_TINY)
        source_line = source if len(source) <= 54 else source[:51] + "..."
        draw.text((x0 + 150, y + 47), source_line, fill=MUTED, font=F_TINY)

        draw.line((bar_x, y + 28, bar_x + bar_w, y + 28), fill="#E6E5DF", width=14)
        fill_w = int(bar_w * cite / max_cite)
        draw.line((bar_x, y + 28, bar_x + fill_w, y + 28), fill=color, width=18)
        draw.text((bar_x + fill_w + 18, y + 12), str(cite), fill=INK, font=F_LABEL)

    draw.text((90, 1075), "Bar length = Lens.org citing works count. Use this as a first-pass milestone signal, then combine with burst, centrality, and cluster-position evidence.", fill=MUTED, font=F_SMALL)
    save(img, "citation_network.png")


def main():
    df = load_data()
    draw_keyword_cooccurrence(df)
    draw_author_collaboration(df)
    draw_country_distribution(df)
    draw_citation_network(df)


if __name__ == "__main__":
    main()
