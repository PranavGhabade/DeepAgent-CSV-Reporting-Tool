"""
Markdown Parser

Parses the markdown report into logical sections.

This module DOES NOT render anything.

It only prepares structured content for the renderers.
"""

import re


SECTION_MAP = {
    "Executive Summary": "executive_summary",
    "Dataset Overview": "dataset_overview",
    "Statistical Findings": "statistical_findings",
    "Visual Analysis": "visual_analysis",
    "Business Insights": "business_insights",
    "Recommendations": "recommendations",
    "Conclusion": "conclusion",
}


def clean_markdown(text: str) -> str:
    """
    Remove markdown artefacts that interfere with ReportLab.
    """

    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)

    text = text.replace("```markdown", "")
    text = text.replace("```", "")

    return text.strip()


def parse_report(report_text: str):
    """
    Split the report into sections.

    Returns
    -------
    dict

    {
        section_name: [
            line1,
            line2,
            ...
        ]
    }
    """

    report_text = clean_markdown(report_text)

    lines = report_text.splitlines()

    sections = {}

    current_section = None

    for line in lines:

        line = line.rstrip()

        # Ignore main title
        if line.startswith("# "):
            continue

        # Detect section
        if line.startswith("## "):

            heading = line[3:].strip()

            current_section = SECTION_MAP.get(
                heading,
                heading.lower().replace(" ", "_"),
            )

            sections[current_section] = []

            continue

        if current_section:

            # Ignore horizontal rules
            if line.strip() == "---":
                continue

            # Ignore blank lines
            if not line.strip():
                continue

            sections[current_section].append(line.strip())

    return sections