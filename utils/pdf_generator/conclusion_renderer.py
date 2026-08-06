"""
Conclusion Renderer

Renders the Conclusion section.
"""

from reportlab.platypus import Spacer
from reportlab.lib.units import inch

from utils.pdf_generator.pdf_components import (
    create_section_header,
    create_narrative,
)

from utils.pdf_generator.helpers import (
    clean_inline_markdown,
)


def render_conclusion(lines):
    """
    Render the conclusion section.
    """

    story = []

    story.append(
        create_section_header("Conclusion")
    )

    paragraph = []

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        paragraph.append(
            clean_inline_markdown(line)
        )

    if paragraph:

        story.append(
            create_narrative(
                " ".join(paragraph)
            )
        )

    story.append(
        Spacer(1, 0.20 * inch)
    )

    return story