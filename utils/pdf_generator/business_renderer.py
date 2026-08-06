"""
Business Insights Renderer

Renders the Business Insights section.
"""

from reportlab.platypus import Spacer
from reportlab.lib.units import inch

from utils.pdf_generator.pdf_components import (
    create_section_header,
    create_subheading,
    create_narrative,
)

from utils.pdf_generator.helpers import (
    is_heading,
    get_heading_text,
    is_bullet,
    strip_bullet,
    clean_inline_markdown,
)


def render_business_insights(lines):
    """
    Render the Business Insights section.
    """

    story = []

    story.append(
        create_section_header("Business Insights")
    )

    paragraph_buffer = []

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        # -----------------------------------------
        # New Heading
        # -----------------------------------------

        if is_heading(line):

            # Flush previous paragraph
            if paragraph_buffer:

                story.append(
                    create_narrative(
                        " ".join(paragraph_buffer)
                    )
                )

                story.append(
                    Spacer(1, 0.12 * inch)
                )

                paragraph_buffer = []

            story.append(
                create_subheading(
                    get_heading_text(line)
                )
            )

            story.append(
                Spacer(1, 0.05 * inch)
            )

            continue

        # -----------------------------------------
        # Bullet Point
        # -----------------------------------------

        if is_bullet(line):

            # Flush paragraph before bullets
            if paragraph_buffer:

                story.append(
                    create_narrative(
                        " ".join(paragraph_buffer)
                    )
                )

                story.append(
                    Spacer(1, 0.08 * inch)
                )

                paragraph_buffer = []

            story.append(
                create_narrative(
                    "• " + clean_inline_markdown(
                        strip_bullet(line)
                    )
                )
            )

            continue

        # -----------------------------------------
        # Normal Paragraph
        # -----------------------------------------

        paragraph_buffer.append(
            clean_inline_markdown(line)
        )

    # -----------------------------------------
    # Flush remaining paragraph
    # -----------------------------------------

    if paragraph_buffer:

        story.append(
            create_narrative(
                " ".join(paragraph_buffer)
            )
        )

    return story