"""
Recommendation Renderer

Renders the Recommendations section.
"""

import re

from reportlab.platypus import Spacer
from reportlab.lib.units import inch

from utils.pdf_generator.pdf_components import (
    create_section_header,
    create_narrative,
)

from utils.pdf_generator.helpers import (
    strip_bullet,
    clean_inline_markdown,
)


def render_recommendations(lines):
    """
    Render recommendation section.
    """

    story = []

    story.append(
        create_section_header("Recommendations")
    )

    recommendation_number = 1

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        text = clean_inline_markdown(
            strip_bullet(line)
        )

        # Remove existing numbering if the LLM already generated it
        text = re.sub(r"^\d+\.\s*", "", text)

        story.append(
            create_narrative(
                f"<b>{recommendation_number}.</b> {text}"
            )
        )

        story.append(
            Spacer(1, 0.08 * inch)
        )

        recommendation_number += 1

    return story