from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, Line, String

BASE = Path(__file__).resolve().parent
source = BASE / "PERSONALIZED_PLAN_8H_WEEK.md"
out_pdf = BASE / "PERSONALIZED_PLAN_8H_WEEK.pdf"

text = source.read_text(encoding="utf-8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=colors.HexColor("#0f172a")))
styles.add(ParagraphStyle(name="PlanHeading2", parent=styles["Heading2"], fontSize=13, leading=16, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#0f172a")))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontSize=9.5, leading=12.5, textColor=colors.HexColor("#111827")))
styles.add(ParagraphStyle(name="PlanCode", parent=styles["Code"], fontName="Courier", fontSize=8.2, leading=10.2, backColor=colors.HexColor("#f8fafc"), borderColor=colors.HexColor("#dbeafe"), borderPadding=6, borderWidth=0.5))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.2, leading=10.4, textColor=colors.HexColor("#475569")))
styles.add(ParagraphStyle(name="PlanBullet", parent=styles["BodyText"], fontSize=9.2, leading=11.2, leftIndent=10, bulletIndent=0, textColor=colors.HexColor("#111827")))


def draw_skill_chart():
    data = [
        ("Python & Backend", 4, 25),
        ("DB & SQL", 2, 25),
        ("Frontend", 1, 25),
        ("DevOps", 7, 25),
        ("API & Web", 2, 25),
        ("Git", 3, 25),
        ("AI & LLM", 2, 25),
    ]
    drawing = Drawing(480, 180)
    drawing.add(Rect(0, 0, 480, 180, fillColor=colors.HexColor("#f8fbff"), strokeColor=colors.HexColor("#dbeafe"), strokeWidth=1))
    drawing.add(Line(70, 30, 70, 150, strokeColor=colors.HexColor("#cbd5e1"), strokeWidth=1))
    drawing.add(Line(70, 150, 430, 150, strokeColor=colors.HexColor("#cbd5e1"), strokeWidth=1))
    for index, (label, value, max_value) in enumerate(data):
        y = 35 + index * 16
        width = 20 + (value / max_value) * 140
        drawing.add(Rect(90, y, width, 10, fillColor=colors.HexColor("#2563eb"), strokeWidth=0))
        drawing.add(String(85, y + 1, label, fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#334155")))
        drawing.add(String(240 + width, y + 1, f"{value}/{max_value}", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#64748b")))
    return drawing


def draw_weekly_rhythm():
    drawing = Drawing(480, 150)
    drawing.add(Rect(0, 0, 480, 150, fillColor=colors.HexColor("#f8fbff"), strokeColor=colors.HexColor("#dbeafe"), strokeWidth=1))
    boxes = [(70, 70, 90, 40, "Plan"), (200, 70, 90, 40, "Build"), (330, 70, 90, 40, "Review")]
    for x, y, w, h, label in boxes:
        drawing.add(Rect(x, y, w, h, fillColor=colors.HexColor("#2563eb"), strokeWidth=0))
        drawing.add(String(x + w / 2, y + h / 2 + 3, label, fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=colors.white))
    return drawing


def draw_architecture():
    drawing = Drawing(500, 180)
    drawing.add(Rect(0, 0, 500, 180, fillColor=colors.HexColor("#f8fbff"), strokeColor=colors.HexColor("#dbeafe"), strokeWidth=1))
    boxes = [
        (40, 70, 90, 45, "User"),
        (180, 70, 110, 45, "Flask API"),
        (340, 70, 110, 45, "Database"),
        (470, 70, 70, 45, "CI/CD"),
    ]
    for x, y, w, h, label in boxes:
        drawing.add(Rect(x, y, w, h, fillColor=colors.HexColor("#14b8a6"), strokeWidth=0))
        drawing.add(String(x + w / 2, y + h / 2 + 3, label, fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=colors.white))
    drawing.add(Line(130, 92, 180, 92, strokeColor=colors.HexColor("#64748b"), strokeWidth=1.5))
    drawing.add(Line(290, 92, 340, 92, strokeColor=colors.HexColor("#64748b"), strokeWidth=1.5))
    drawing.add(Line(450, 92, 470, 92, strokeColor=colors.HexColor("#64748b"), strokeWidth=1.5))
    return drawing


def clean_inline(text):
    text = text.replace("`", "")
    text = text.replace("---", "")
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    return text.strip()


def split_markdown_blocks(markdown_text):
    blocks = []
    lines = markdown_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i].rstrip())
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(("code", "\n".join(code_lines)))
            continue

        if line.strip() == "---":
            blocks.append(("rule", None))
            i += 1
            continue

        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title_text = line[level:].strip()
            blocks.append(("heading", (level, title_text)))
            i += 1
            continue

        if re.match(r"^(\s*)([-*]|\d+\.)\s+", line):
            bullet_lines = []
            while i < len(lines) and (not lines[i].strip() or re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i])):
                if lines[i].strip():
                    bullet_lines.append(lines[i].strip())
                i += 1
            blocks.append(("bullet", "\n".join(bullet_lines)))
            continue

        paragraph_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("```") and lines[i].strip() != "---":
            if re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i]):
                break
            paragraph_lines.append(lines[i].strip())
            i += 1
        if paragraph_lines:
            blocks.append(("paragraph", "\n".join(paragraph_lines)))

    return blocks


def build_story(text):
    story = []
    story.append(Paragraph("Personalized Development Plan", styles["TitleStyle"]))
    story.append(Paragraph("Balazs' Tech Mastery & Product Launch", styles["Body"]))
    story.append(Paragraph("Overall score: 30/200 • Beginner path • 8h/week delivery rhythm", styles["Small"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(KeepTogether([
        Paragraph("Skill Snapshot", styles["PlanHeading2"]),
        draw_skill_chart(),
        Spacer(1, 0.2 * cm),
    ]))

    story.append(KeepTogether([
        Paragraph("Weekly Rhythm", styles["PlanHeading2"]),
        draw_weekly_rhythm(),
        Spacer(1, 0.2 * cm),
    ]))

    story.append(KeepTogether([
        Paragraph("Target System Architecture", styles["PlanHeading2"]),
        draw_architecture(),
        Spacer(1, 0.25 * cm),
    ]))

    story.append(Paragraph("Key idea: build the product while building technical skill in parallel, using strong project management habits to stay focused inside an 8-hour weekly budget.", styles["Body"]))
    story.append(Spacer(1, 0.25 * cm))

    for kind, payload in split_markdown_blocks(text):
        if kind == "heading":
            level, title = payload
            if level == 1:
                story.append(Paragraph(title, styles["TitleStyle"]))
            elif level == 2:
                story.append(Paragraph(title, styles["PlanHeading2"]))
            else:
                story.append(Paragraph(title, styles["Body"]))
        elif kind == "bullet":
            for item in [line.strip() for line in payload.splitlines() if line.strip()]:
                clean_item = clean_inline(item)
                if clean_item.startswith("- "):
                    clean_item = clean_item[2:]
                story.append(Paragraph(f"• {clean_item}", styles["PlanBullet"]))
        elif kind == "code":
            code_text = clean_inline(payload).replace("\n", "<br/>")
            story.append(Paragraph(code_text, styles["PlanCode"]))
        elif kind == "rule":
            story.append(Spacer(1, 0.12 * cm))
        else:
            paragraph = clean_inline(payload).replace("\n", "<br/>")
            if paragraph:
                story.append(Paragraph(paragraph, styles["Body"]))
        story.append(Spacer(1, 0.06 * cm))
    return story


doc = SimpleDocTemplate(str(out_pdf), pagesize=A4, rightMargin=2.2 * cm, leftMargin=2.2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm)
story = build_story(text)
doc.build(story)
print(f"Created {out_pdf}")
