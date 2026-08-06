"""
Visual Analysis Renderer

Responsible for rendering the Visual Analysis section.

Phase 1:
Parses the markdown visual section into structured figure objects.
"""

from __future__ import annotations
from utils.pdf_generator.helpers import clean_inline_markdown
import os
from reportlab.platypus import (
    Image,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.units import inch
from utils.pdf_generator.pdf_components import (
    create_section_header,
    create_subheading,
    create_figure_caption,
    create_figure_description,
    create_ai_insight_box,
)


def parse_visual_section(lines):
    """
    Convert the Visual Analysis markdown section into
    structured figure dictionaries.

    Parameters
    ----------
    lines : list[str]

    Returns
    -------
    list

    Example
    -------
    [
        {
            "title": "Figure 1. Sales Trend",
            "description": "...",
            "analysis": "..."
        }
    ]
    """

    figures = []

    current = None
    mode = None

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        # -----------------------------------------
        # New Figure
        # -----------------------------------------

        if line.startswith("###"):

            if current:
                figures.append(current)

            current = {
                "title": clean_inline_markdown(
                    line.replace("###", "").strip()
                ),
                "description": "",
                "analysis": "",
            }

            mode = None
            continue

        # -----------------------------------------
        # Description
        # -----------------------------------------

        if line.lower().startswith("description"):

            mode = "description"
            continue

        # -----------------------------------------
        # Analysis
        # -----------------------------------------

        if line.lower().startswith("analysis"):

            mode = "analysis"
            continue

        # -----------------------------------------
        # Store Text
        # -----------------------------------------

        if current is None:
            continue

        if mode == "description":

            if current["description"]:
                current["description"] += " "

            current["description"] += clean_inline_markdown(line)

        elif mode == "analysis":

            if current["analysis"]:
                current["analysis"] += " "

            current["analysis"] += clean_inline_markdown(line)

    if current:
        figures.append(current)

    return figures


def render_visual_analysis(
    visual_lines,
    chart_paths,
):
    """
    Render the Visual Analysis section.

    Parameters
    ----------
    visual_lines : list[str]

    chart_paths : dict

    Returns
    -------
    list
        ReportLab Flowables.
    """

    story = []

    story.append(
        create_section_header("Visual Analysis")
    )

    figures = parse_visual_section(visual_lines)

    charts = list(chart_paths.values())

    for index, figure in enumerate(figures):

        # -----------------------------
        # Figure Heading
        # -----------------------------

        story.append(
            create_subheading(
                figure["title"]
            )
        )

        story.append(Spacer(1, 0.10 * inch))

        # -----------------------------
        # Figure Image
        # -----------------------------

        if index < len(charts):

            image_path = charts[index]

            if os.path.exists(image_path):

                img = Image(
                    image_path,
                    width=6.2 * inch,
                    height=3.8 * inch,
                )

                image_table = Table(
                    [[img]],
                    colWidths=[6.4 * inch],
                )

                image_table.setStyle(
                    TableStyle(
                        [
                            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D9D9D9")),
                            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                            ("TOPPADDING", (0, 0), (-1, -1), 8),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ]
                    )
                )

                story.append(image_table)

                story.append(
                    Spacer(1, 0.08 * inch)
                )

                story.append(
                    create_figure_caption(
                        figure["title"]
                    )
                )

        # -----------------------------
        # Description Box
        # -----------------------------

        if figure["description"]:

            story.append(

                create_figure_description(
                    figure["description"]
                )

            )

            story.append(
                Spacer(1, 0.12 * inch)
            )

        # -----------------------------
        # AI Insight Box
        # -----------------------------

        if figure["analysis"]:

            story.append(

                create_ai_insight_box(
                    figure["analysis"]
                )

            )

        story.append(
            Spacer(1, 0.30 * inch)
        )

    return story