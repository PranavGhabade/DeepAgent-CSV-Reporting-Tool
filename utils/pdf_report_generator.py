"""
PDF Report Generator

Main orchestrator for building the PDF report.
"""

from __future__ import annotations

import os

from reportlab.platypus import (
    SimpleDocTemplate,
    PageBreak,
)
from utils.pdf_generator.pdf_components import (
    draw_header_footer,
)

from reportlab.lib.units import inch

from utils.pdf_generator.parser import parse_report
from utils.pdf_generator.chart_manager import ChartManager

from utils.pdf_generator.cover_page import create_cover_page
from utils.pdf_generator.table_of_contents import create_table_of_contents

from utils.pdf_generator.overview_renderer import render_dataset_overview
from utils.pdf_generator.statistics_renderer import render_statistics
from utils.pdf_generator.visual_renderer import render_visual_analysis
from utils.pdf_generator.business_renderer import render_business_insights
from utils.pdf_generator.recommendation_renderer import render_recommendations
from utils.pdf_generator.conclusion_renderer import render_conclusion
from datetime import datetime


OUTPUT_DIR = "outputs"
OUTPUT_PDF = os.path.join(
    OUTPUT_DIR,
    "report.pdf",
)


def generate_pdf_report(memory):
    """
    Generate the final PDF report.
    """

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    report_text = memory.get_report("markdown")

    chart_paths = memory.get_analysis("visualizations") or {}

    profile = memory.get_analysis("profile") or {}

    sections = parse_report(report_text)

    chart_manager = ChartManager(chart_paths)

    charts = chart_manager.get_resolved_charts()

    story = []

    # Cover

    story.extend(
    create_cover_page(
        profile,
        datetime.now().strftime("%d %B %Y, %I:%M %p"),))

    # Table of Contents

    story.extend(
        create_table_of_contents()
    )

    story.append(PageBreak())

    # Dataset Overview

    story.extend(
        render_dataset_overview(
            sections.get("dataset_overview", []),
            profile,
        )
    )

    # Statistical Findings

    story.extend(
        render_statistics(
            sections.get("statistical_findings", [])
        )
    )

    # Visual Analysis

    story.extend(
        render_visual_analysis(
            sections.get("visual_analysis", []),
            charts,
        )
    )

    # Business Insights

    story.extend(
        render_business_insights(
            sections.get("business_insights", [])
        )
    )

    # Recommendations

    story.extend(
        render_recommendations(
            sections.get("recommendations", [])
        )
    )

    # Conclusion

    story.extend(
        render_conclusion(
            sections.get("conclusion", [])
        )
    )

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=1.15 * inch,
        bottomMargin=0.6 * inch,
    )

    doc.build(
    story,
    onFirstPage=draw_header_footer,
    onLaterPages=draw_header_footer,
    )

    return OUTPUT_PDF