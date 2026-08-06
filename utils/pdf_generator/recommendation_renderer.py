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

        raw_line = raw_line.strip()

        if not raw_line:
            continue

        # -----------------------------------------
        # Split multiple bullets generated in one line
        # -----------------------------------------

        if "•" in raw_line:

            recommendations = [
                part.strip()
                for part in raw_line.split("•")
                if part.strip()
            ]

        else:

            recommendations = [raw_line]

        # -----------------------------------------
        # Process each recommendation
        # -----------------------------------------

        for recommendation in recommendations:

            text = recommendation

            # Remove existing numbering like:
            # 1. Recommendation
            text = re.sub(
                r"^\d+\.\s*",
                "",
                text,
            )

            # Remove markdown bullets
            text = re.sub(
                r"^[-*]\s*",
                "",
                text,
            )

            # Remove any remaining bullet character
            text = text.replace("•", "").strip()

            # Remove markdown formatting
            text = (
                text.replace("**", "")
                    .replace("*", "")
                    .replace("`", "")
                    .strip()
            )

            if not text:
                continue

            story.append(
                create_narrative(
                    f"<b>{recommendation_number}.</b> {text}"
                )
            )

            story.append(
                Spacer(1, 0.12 * inch)
            )

            recommendation_number += 1

    return story