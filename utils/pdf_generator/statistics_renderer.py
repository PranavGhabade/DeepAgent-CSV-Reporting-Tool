"""
Statistics Renderer

Renders the Statistical Findings section.
"""

from reportlab.platypus import Spacer
from reportlab.lib.units import inch

from utils.pdf_generator.pdf_components import (
    create_section_header,
    create_narrative,
    create_styled_table,
)

from utils.pdf_generator.helpers import (
    is_table_line,
    is_heading,
    get_heading_text,
    parse_markdown_table,
)


def render_statistics(lines):
    """
    Convert the Statistical Findings markdown section
    into ReportLab flowables.
    """

    story = []

    # -----------------------------------------
    # Section Heading
    # -----------------------------------------

    story.append(
        create_section_header("Statistical Findings")
    )

    i = 0

    while i < len(lines):

        line = lines[i].strip()
        print(repr(line))

        # -----------------------------------------
        # Skip Blank Lines
        # -----------------------------------------

        if not line:
            i += 1
            continue

        # -----------------------------------------
        # Markdown Heading
        # Example:
        # ### Table 1. Key Traffic Metrics Summary
        # -----------------------------------------

        if is_heading(line):

            story.append(
                create_narrative(
                    f"<font size='11'><b>{get_heading_text(line)}</b></font>"
                )
            )

            story.append(
                Spacer(1, 0.08 * inch)
            )

            i += 1
            continue

        # -----------------------------------------
        # Markdown Table
        # -----------------------------------------

        if is_table_line(line):

            table_lines = []

            while i < len(lines):

                current = lines[i].strip()

                if not is_table_line(current):
                    break

                table_lines.append(current)

                i += 1

            table_data = parse_markdown_table(table_lines)

            if table_data:

                story.append(
                    create_styled_table(table_data)
                )

                story.append(
                    Spacer(1, 0.18 * inch)
                )

            continue

        # -----------------------------------------
        # Normal Paragraph
        # -----------------------------------------

        story.append(
            create_narrative(line)
        )

        story.append(
            Spacer(1, 0.08 * inch)
        )

        i += 1

    return story