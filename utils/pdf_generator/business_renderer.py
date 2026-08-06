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
    create_bullet,
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

        raw_line = raw_line.strip()

        if not raw_line:
            continue

        # -----------------------------------------
        # Split multiple bullets generated in one line
        # -----------------------------------------
        if "•" in raw_line:
            segments = [
                f"• {part.strip()}"
                for part in raw_line.split("•")
                if part.strip()
            ]
        else:
            segments = [raw_line]

        # -----------------------------------------
        # Process each segment independently
        # -----------------------------------------
        for line in segments:
            line = line.strip()
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
            if is_bullet(line) or line.startswith("•"):

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

                # FIXED: Use the specialized bullet renderer so it adds lists sequentially
                story.append(
                    create_bullet(
                        clean_inline_markdown(
                            strip_bullet(line)
                        )
                    )
                )

                story.append(
                    Spacer(1, 0.06 * inch)
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















# """
# Business Insights Renderer

# Renders the Business Insights section.
# """

# from reportlab.platypus import Spacer
# from reportlab.lib.units import inch

# from utils.pdf_generator.pdf_components import (
#     create_section_header,
#     create_subheading,
#     create_narrative,
#     create_bullet,
# )

# from utils.pdf_generator.helpers import (
#     is_heading,
#     get_heading_text,
#     is_bullet,
#     strip_bullet,
#     clean_inline_markdown,
# )


# def render_business_insights(lines):
#     """
#     Render the Business Insights section.
#     """

#     story = []

#     story.append(
#         create_section_header("Business Insights")
#     )

#     paragraph_buffer = []

#     for raw_line in lines:

#         raw_line = raw_line.strip()

#         if not raw_line:
#             continue

#         # -----------------------------------------
#         # Split multiple bullets generated in one line
#         # -----------------------------------------

#         if "•" in raw_line:

#             segments = [
#                 f"• {part.strip()}"
#                 for part in raw_line.split("•")
#                 if part.strip()
#             ]

#         else:

#             segments = [raw_line]

#         # -----------------------------------------
#         # Process each segment independently
#         # -----------------------------------------

#         for line in segments:

#             # -----------------------------------------
#             # New Heading
#             # -----------------------------------------

#             if is_heading(line):

#                 # Flush previous paragraph
#                 if paragraph_buffer:

#                     story.append(
#                         create_narrative(
#                             " ".join(paragraph_buffer)
#                         )
#                     )

#                     story.append(
#                         Spacer(1, 0.12 * inch)
#                     )

#                     paragraph_buffer = []

#                 story.append(
#                     create_subheading(
#                         get_heading_text(line)
#                     )
#                 )

#                 story.append(
#                     Spacer(1, 0.05 * inch)
#                 )

#                 continue

#             # -----------------------------------------
#             # Bullet Point
#             # -----------------------------------------

#             if is_bullet(line):

#                 # Flush paragraph before bullets
#                 if paragraph_buffer:

#                     story.append(
#                         create_narrative(
#                             " ".join(paragraph_buffer)
#                         )
#                     )

#                     story.append(
#                         Spacer(1, 0.08 * inch)
#                     )

#                     paragraph_buffer = []

#                 # story.append(
#                 #     create_bullet(
#                 #         "• " + clean_inline_markdown(
#                 #             strip_bullet(line)
#                 #         )
#                 #     )
#                 # )

#                 # story.append(
#                 #     Spacer(1, 0.05 * inch)
#                 # )


#                 story.append(
#                     create_narrative(
#                         clean_inline_markdown(
#                             strip_bullet(line)
#                         )
#                     )
#                 )

#                 story.append(
#                     Spacer(1, 0.10 * inch)
#                 )

#                 continue

#             # -----------------------------------------
#             # Normal Paragraph
#             # -----------------------------------------

#             paragraph_buffer.append(
#                 clean_inline_markdown(line)
#             )

#     # -----------------------------------------
#     # Flush remaining paragraph
#     # -----------------------------------------

#     if paragraph_buffer:

#         story.append(
#             create_narrative(
#                 " ".join(paragraph_buffer)
#             )
#         )

#     return story