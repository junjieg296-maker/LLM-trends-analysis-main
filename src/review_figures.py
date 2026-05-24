import os

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1800
HEIGHT = 1050
BG = "#F8F7F2"
INK = "#24313B"
MUTED = "#66757F"
GRID = "#D9DDD7"
BLUE = "#2F6F9F"
TEAL = "#3B9C8A"
GOLD = "#C99A2E"
CORAL = "#D66A4A"
PLUM = "#8B5A8C"
GREEN = "#5A8F55"


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = os.path.join("C:\\Windows\\Fonts", name)
    return ImageFont.truetype(path, size=size)


F_TITLE = font(50, True)
F_SUB = font(27)
F_HEAD = font(30, True)
F_TEXT = font(24)
F_SMALL = font(20)


def rounded(draw, box, fill, outline=None, width=2, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw, text, x, y, width, fnt, fill=INK, gap=7):
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            line = test
        else:
            draw.text((x, y), line, fill=fill, font=fnt)
            y += fnt.size + gap
            line = word
    if line:
        draw.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + gap
    return y


def draw_arrow(draw, start, end, color=GRID, width=5):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0:
            points = [(x2, y2), (x2 - 18, y2 - 10), (x2 - 18, y2 + 10)]
        else:
            points = [(x2, y2), (x2 + 18, y2 - 10), (x2 + 18, y2 + 10)]
    else:
        if dy > 0:
            points = [(x2, y2), (x2 - 10, y2 - 18), (x2 + 10, y2 - 18)]
        else:
            points = [(x2, y2), (x2 - 10, y2 + 18), (x2 + 10, y2 + 18)]
    draw.polygon(points, fill=color)


def make_review_framework():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    draw.text((90, 55), "Bibliometric Review Framework for LLM Multi-Agent Collaboration", fill=INK, font=F_TITLE)
    draw.text((92, 125), "From data evidence to technical narratives and future research agenda", fill=MUTED, font=F_SUB)
    draw.line((90, 175, WIDTH - 90, 175), fill=GRID, width=3)

    stages = [
        ("Data Layer", "522 cleaned Lens.org records\n2020-2026 / Article, Review, Conference Paper", BLUE),
        ("Bibliometric Evidence", "Annual trend, citation impact, keyword co-occurrence, collaboration network", TEAL),
        ("Theme Structure", "LLM foundation, agentic architecture, RAG/RL enhancement, governance and applications", GOLD),
        ("Technical Narratives", "Planning workflows, self-driving labs, human-AI teaming, clinical and robotic agents", CORAL),
        ("Research Agenda", "Benchmarking, explainability, vertical validation, safety and accountability", PLUM),
    ]

    x = 85
    y = 265
    box_w = 286
    box_h = 210
    gap = 36
    centers = []
    for title, body, color in stages:
        rounded(draw, (x, y, x + box_w, y + box_h), "#FFFFFF", "#DDD8CE", 2, 22)
        draw.rectangle((x, y, x + box_w, y + 16), fill=color)
        draw.text((x + 24, y + 38), title, fill=color, font=F_HEAD)
        yy = y + 90
        for line in body.split("\n"):
            yy = wrap(draw, line, x + 24, yy, box_w - 48, F_SMALL, MUTED, 5)
        centers.append((x + box_w // 2, y + box_h // 2))
        x += box_w + gap

    for a, b in zip(centers, centers[1:]):
        draw_arrow(draw, (a[0] + box_w // 2 - 5, a[1]), (b[0] - box_w // 2 + 5, b[1]), "#C7CBC6", 5)

    draw.text((90, 565), "Narrative translation", fill=INK, font=F_HEAD)
    draw.text((90, 610), "The review does not list topics mechanically. Bibliometric signals are used to decide which technical storylines deserve full discussion.", fill=MUTED, font=F_TEXT)

    pillars = [
        ("Task Planning", "Natural-language goals -> executable multi-agent workflows", BLUE),
        ("Scientific Discovery", "Literature, hypothesis, experiment, analysis and reporting loops", TEAL),
        ("Human-AI Teaming", "Human oversight, explanation, correction and responsibility", GOLD),
        ("Vertical Agents", "Clinical, robotic, chemical and engineering applications", CORAL),
    ]
    px = 110
    py = 705
    for title, body, color in pillars:
        rounded(draw, (px, py, px + 375, py + 175), "#FFFFFF", "#E1DDD5", 2, 16)
        draw.ellipse((px + 24, py + 28, px + 62, py + 66), fill=color)
        draw.text((px + 80, py + 25), title, fill=INK, font=F_HEAD)
        wrap(draw, body, px + 28, py + 88, 320, F_SMALL, MUTED, 6)
        px += 410

    draw.text((90, 955), "Figure. Review logic used in this mini review: bibliometric results define the chapter structure, and technical interpretation turns clusters into research narratives.", fill=MUTED, font=F_SMALL)

    path = os.path.join("outputs", "figures", "review_framework.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, quality=95)
    print(path)


if __name__ == "__main__":
    make_review_framework()
