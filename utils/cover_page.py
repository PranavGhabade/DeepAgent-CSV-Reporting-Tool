from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,)
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

from utils.pdf_styles import BODY_STYLE, TITLE_STYLE


COVER_TITLE = ParagraphStyle(
    "CoverTitle",
    parent=TITLE_STYLE,
    alignment=TA_CENTER,
    fontSize=28,
    leading=34,
    spaceAfter=16,
)

COVER_SUBTITLE = ParagraphStyle(
    "CoverSubTitle",
    parent=BODY_STYLE,
    alignment=TA_CENTER,
    fontSize=14,
    leading=20,
    textColor=colors.HexColor("#555555"),
)

COVER_FOOTER = ParagraphStyle(
    "CoverFooter",
    parent=BODY_STYLE,
    alignment=TA_CENTER,
    textColor=colors.grey,
)


def create_cover_page(report_metadata, generated_on):

    dataset = report_metadata.get("dataset_info", {})

    rows = dataset.get("rows", "-")
    columns = dataset.get("columns", "-")
    duplicates = dataset.get("duplicates_rows", "-")

    story = []

    story.append(Spacer(1, 0.7 * inch))

    story.append(
        Paragraph(
            "ABC Analytics Pvt Ltd",
            COVER_TITLE,
        )
    )

    story.append(
        Paragraph(
            "Data Driven Decision with AI",
            COVER_SUBTITLE,
        )
    )

    story.append(Spacer(1, 0.8 * inch))

    story.append(
        Paragraph(
            "AI Data Analysis Report",
            COVER_TITLE,
        )
    )

    story.append(Spacer(1, 0.4 * inch))

    table_data = [
        ["Generated On", str(generated_on)],
        ["Rows", f"{rows:,}" if isinstance(rows, int) else str(rows)],
        ["Columns", str(columns)],
        ["Duplicate Rows", str(duplicates)],
        ["Version", "1.0"],
    ]

    table = Table(
        table_data,
        colWidths=[2.2 * inch, 3.2 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9D9D9")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F5F5F5")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 2.2 * inch))

    story.append(
        Paragraph(
            "Prepared by",
            COVER_SUBTITLE,
        )
    )

    story.append(
        Paragraph(
            "ABC Analytics Pvt Ltd",
            COVER_TITLE,
        )
    )

    story.append(
        Paragraph(
            "Confidential",
            COVER_FOOTER,
        )
    )

    return story
