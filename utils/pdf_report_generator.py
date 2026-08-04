import os
import re
from reportlab.platypus import Paragraph, Spacer, Image, SimpleDocTemplate, KeepTogether, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from utils.pdf_styles import (
    TITLE_STYLE,
    BODY_STYLE,
    BULLET_STYLE,
    HEADING_STYLE, 
    HIGHLIGHT_STYLE
)
from utils.pdf_components import (
    create_section_header, 
    create_subheading,
    create_figure_caption,
    create_narrative,
    create_styled_table,
    create_ai_insight_box,
    create_kpi_cards,
    create_figure_description,
)

from utils.cover_page import create_cover_page
from utils.table_of_contents import create_table_of_contents

styles = getSampleStyleSheet()


def clean_report(text):
    text = re.sub(r"\*\*", "", text)
    text = text.replace("```", "")
    return text


def add_footer(canvas, doc):
    width, _ = doc.pagesize
    canvas.setStrokeColor(colors.grey)
    canvas.line(40, 45, width - 40, 45)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(40, 30, "ABC Analytics Pvt Ltd")
    canvas.drawCentredString(width / 2, 30, "Confidential")
    canvas.drawRightString(width - 40, 30, f"Page {doc.page}")

def add_page_elements(canvas, doc):
    canvas.saveState()

    page_width, page_height = doc.pagesize

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        canvas.drawImage(
            logo_path,
            doc.leftMargin,
            page_height - 0.85 * inch,  
            width=0.65 * inch,
            height=0.65 * inch,
            preserveAspectRatio=True,
            mask="auto",
        )
        
    canvas.setFont("Helvetica-Bold", 22)
    canvas.drawString(
        doc.leftMargin + 0.8 * inch,
        page_height - 0.50 * inch,      
        "ABC Analytics Pvt Ltd"
    )

    # SUBHEADING
    canvas.setFont("Helvetica", 11)
    canvas.setFillColor(colors.grey)
    canvas.drawString(
        doc.leftMargin + 0.8 * inch,
        page_height - 0.78 * inch,      
        "Data Driven Decision with AI"
    )

    canvas.setFillColor(colors.black)

    canvas.line(
        doc.leftMargin,
        page_height - 1.05 * inch,
        page_width - doc.rightMargin,
        page_height - 1.05 * inch,
    )

    add_footer(canvas, doc)
    canvas.restoreState()



def generate_pdf_report(memory, output_path="outputs/report.pdf",):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    from datetime import datetime

    report_text = memory.get_report("markdown")

    chart_paths = memory.get_analysis("visualizations") or {}

    profile = memory.get_analysis("profile") or {}

    statistics = memory.get_analysis("statistics") or {}

    business = memory.get_analysis("business_insights") or {}

    generated_on = datetime.now().strftime("%d %B %Y %H:%M")

    report_metadata = {
        "dataset_info": profile.get("dataset_info", {})
    }

    doc = SimpleDocTemplate(
        output_path,
        topMargin=1.35 * inch,
        bottomMargin=0.7 * inch,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
    )

    story = []

    story.extend(create_cover_page(report_metadata, generated_on,))
    story.append(PageBreak())
    story.extend(create_table_of_contents())
    story.append(PageBreak())

    last_chart_rendered = False
    
    dataset_info = report_metadata.get("dataset_info", {})

    rows = dataset_info.get("rows", "---")
    columns = dataset_info.get("columns", "---")
    duplicates = dataset_info.get("duplicate_rows", "---") 

    resolved_chart_paths = {}

    print(type(chart_paths))
    print(chart_paths)

    for title_key, chart_path in (chart_paths or {}).items():
        if not isinstance(chart_path, str):
            continue
        resolved_path = (
            chart_path
            if os.path.isabs(chart_path)
            else os.path.abspath(chart_path)
        )

        if os.path.exists(resolved_path):
            resolved_chart_paths[title_key] = resolved_path
        else:
            print(f"Skipping missing chart: {title_key}")

    report_text = clean_report(report_text)

    lines = report_text.splitlines()
    i = 0

    figure_number = 0
    
    print("\n==========Resolved CHARcreaTS=========")
    for k in resolved_chart_paths.keys():
        print(repr(k))

    while i < len(lines):
        print(f"Processing line {i}: {repr(lines[i])}")
        line = lines[i].rstrip()

        if line.strip() == "---":
            i += 1
            continue

        if not line:
            i += 1
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:], TITLE_STYLE))
            story.append(Spacer(1, 0.08 * inch))
            i += 1
            continue

        if line.startswith("## "):
            highlight_counter = 1
            story.append(create_section_header(line[3:]))
            story.append(Spacer(1, 0.06 * inch))
            if line[3:].strip().lower() == "visual analysis":
                for chart_name, chart_path in resolved_chart_paths.items():

                    if not os.path.exists(chart_path):
                        continue

                    story.append(
                        Paragraph(
                            chart_name.replace("_", " "),
                            HEADING_STYLE,
                        )
                    )

                    story.append(Spacer(1,0.05*inch))

                    img = Image(
                        chart_path,
                        width=6.1*inch,
                        height=3.4*inch,
                    )

                    img.hAlign = "CENTER"

                    story.append(img)

                    story.append(Spacer(1,0.18*inch))
            i += 1
            continue

        if line.startswith("### "):
            analysis_title = line[4:].strip()
            section_items = []
            section_items.append(create_subheading(analysis_title))
            section_items.append(Spacer(1, 0.05 * inch))

            chart_path = None

            for key, value in resolved_chart_paths.items():

                normalized_key = (
                    key.lower()
                    .replace("_", " ")
                    .replace("-", " ")
                )

                words = analysis_title.lower().split()

                matches = sum(
                    word in normalized_key
                    for word in words
                    if len(word) > 3
                )

                if matches >= 2:
                    chart_path = value
                    break

            print(f"Looking for: {analysis_title}")
            print(f"Matched chart: {chart_path}")

            if chart_path:
                figure_number += 1
                last_chart_rendered = True

                chart = Image(
                    chart_path,
                    width=6.2 * inch,
                    height=3.3 * inch,
                    )
                chart.hAlign = "CENTER"
                
                chart_table = Table([[chart]])
                chart_table.setStyle(
                    TableStyle(
                        [
                            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#C8C8C8")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ]
                        ))

                section_items.append(chart_table)
                section_items.append(Spacer(1, 0.08 * inch))
                section_items.append(create_figure_caption(f"Figure {figure_number}. {analysis_title}"))
                section_items.append(Spacer(1, 0.10 * inch))
            else:
                last_chart_rendered = False
            
            story.append(KeepTogether(section_items))
            i += 1
            continue
            

        if line.startswith('####'):
            heading = line[5:].strip()
            #Figure Caption
            if heading.lower() == "figure caption":
                i += 1

                while i < len(lines) and not lines[i].strip():
                    i += 1

                # Only create figure description if a chart was rendered 
                if (last_chart_rendered and i < len(lines) and lines [i].strip()):
                    story.append(create_figure_description(lines[i].strip()))
                    story.append(Spacer(1, 0.12 * inch))

                i += 1
                continue
            elif heading.lower() == "narrative":
                story.append(create_subheading("Narrative"))
                story.append(Spacer(1, 0.05 * inch))
                i+= 1
                continue
            elif heading.lower() == "ai insight":
                i += 1
                insight = []
                while (
                    i < len(lines)
                    and not lines[i].startswith("#")
                    and not lines[i].startswith("![")
                ):
                    if lines[i].strip():
                        insight.append(lines[i].strip())
                    i += 1

                story.append(
                    create_ai_insight_box(
                        " ".join(insight)
                    )
                )
                story.append(Spacer(1, 0.18 * inch))

                continue
            else:
                story.append(create_subheading(heading))
                story.append(Spacer(1, 0.05 * inch))
                i += 1
                continue

        if line.startswith("|"):
            table_lines = []

            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            data = []

            for row in table_lines:
                if "---" in row:
                    continue
                cells = [
                    c.strip().replace("<br>", "<br/>")
                    for c in row.strip("|").split("|")
                ]

                data.append(cells)

            if data:
                tbl = create_styled_table(data)
                story.append(tbl)
                story.append(Spacer(1, 0.18 * inch))
            continue

        if line.strip().startswith(("- ", "* ")):
            if "highlight_counter" not in locals():
                highlight_counter = 1
            cleaned_text = line.strip()[2:].strip()
            
            story.append(Paragraph(f"<b>{highlight_counter}.</b> {cleaned_text}", HIGHLIGHT_STYLE))
            highlight_counter += 1

            i += 1
            continue

        if re.match(r"^\d+\.\s", line):
            story.append(Paragraph(f"<b>{line}</b>", BODY_STYLE))
            story.append(Spacer(1, 0.02 * inch))
            i += 1
            continue
        # Priority
        if line.startswith("Priority:"):
            story.append(Paragraph(f"<b>{line}</b>", BODY_STYLE))
            story.append(Spacer(1, 0 * inch))
            i += 1
            continue
        # Expected Benefit
        if line.startswith("Expected Benefit"):
            story.append(Paragraph("<b>Expected Benefit:</b>", BODY_STYLE))
            i += 1
            
            if i < len(lines) and lines[i].strip():
                story.append(Paragraph(lines[i].strip(), BODY_STYLE))
                story.append(Spacer(1, 0 * inch))
                i += 1
                
            continue

        story.append(create_narrative(line))
        story.append(Spacer(1, 0.05 * inch))
        i += 1
    
    doc.build(
        story,
        onFirstPage=add_page_elements,
        onLaterPages=add_page_elements,
    )

    return output_path
