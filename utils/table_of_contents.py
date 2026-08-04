from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import inch

from utils.pdf_components import create_section_header
from utils.pdf_styles import BODY_STYLE


def create_table_of_contents():

    story = []

    story.append(create_section_header("Table of Contents"))

    story.append(Spacer(1, 0.20 * inch))

    contents = [
        "1 Executive Summary",
        "2 Dataset Overview",
        "3 Analytical Highlights",
        "4 Analysis Results",
        "5 Overall Findings",
        "6 Recommendations",
        "7 Conclusion",
    ]

    for item in contents:
        story.append(Paragraph(item, BODY_STYLE))
        story.append(Spacer(1, 0.08 * inch))

    return story
