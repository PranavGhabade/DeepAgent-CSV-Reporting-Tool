from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle, HRFlowable, KeepTogether, Image
from reportlab.lib.utils import ImageReader

from utils.pdf_generator.pdf_styles import (
    BODY_STYLE,
    CAPTION_STYLE,
    HEADING_STYLE,
    INSIGHT_STYLE,
    SUBHEADING_STYLE,
    TABLE_HEADER,
)

from reportlab.lib.colors import HexColor

import os

from utils.pdf_generator.pdf_styles import (
    PRIMARY,
    SUBTEXT,
    TEXT,
)


def create_section_header(title):
    return KeepTogether([
        Paragraph(title, HEADING_STYLE),
        HRFlowable(
            width="100%",
            thickness=1.4,
            color=colors.HexColor("#1F4E79"),
            spaceBefore=2,
            spaceAfter=10,
        ),
    ])
    

def create_subheading(title):
    return Paragraph(title, SUBHEADING_STYLE)


def create_figure_caption(text):
    return Paragraph(text, CAPTION_STYLE)


def create_narrative(text):
    return Paragraph(text, BODY_STYLE)


def create_insight_box(text):
    paragraph = Paragraph(
        f"<b>AI Insight</b><br/><br/>{text}",
        INSIGHT_STYLE,
    )

    table = Table([[paragraph]], colWidths=[450])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FA")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#5B9BD5")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return table


def create_styled_table(data):

    if not data:
        return Table([["No Data Available"]])

    # Convert every cell into a Paragraph so text wraps

    formatted_data = []

    for row in data:

        formatted_row = []

        for cell in row:

            formatted_row.append(
                Paragraph(
                    str(cell).replace("\n", "<br/>"),
                    BODY_STYLE,
                )
            )

        formatted_data.append(formatted_row)

    # Dynamic column width calculation

    num_cols = len(formatted_data[0])

    available_width = 6.8 * inch

    if num_cols <= 4:
        col_widths = [available_width / num_cols] * num_cols

    elif num_cols <= 7:
        col_widths = [available_width / num_cols] * num_cols

    else:
        # Many columns
        col_widths = [available_width / num_cols] * num_cols

    table = Table(
        formatted_data,
        colWidths=col_widths,
        repeatRows=1,
    )

    # Font size based on number of columns

    if num_cols <= 5:
        font_size = 9
    elif num_cols <= 8:
        font_size = 8
    else:
        font_size = 7

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, -1), font_size),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.white),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8F9FA"),
                    ],
                ),

                ("LEFTPADDING", (0, 0), (-1, -1), 5),

                ("RIGHTPADDING", (0, 0), (-1, -1), 5),

                ("TOPPADDING", (0, 0), (-1, -1), 5),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

                ("VALIGN", (0, 0), (-1, -1), "TOP"),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("WORDWRAP", (0, 0), (-1, -1), "LTR"),

            ]

        )

    )

    return table


def create_kpi_cards(kpis):
    """
    kpis = [
        ("84550", "Rows"),
        ("61", "Columns"),
        ("2.3%", "Missing"),
        ("0", "Duplicates"),
    ]
    """

    cards = []
    row = []

    for value, label in kpis:
        value_para = Paragraph(
            f"<font size=20><b>{value}</b></font><br/><br/>{label}",
            BODY_STYLE,
        )

        card = Table([[value_para]], colWidths=[1.6 * inch], rowHeights=[0.9 * inch])

        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D9D9D9")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        row.append(card)

    table = Table([row], colWidths=[1.7 * inch] * len(row))

    table.setStyle(
        TableStyle(
            [
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return table

def create_figure_description(text):
    para = Paragraph(text, BODY_STYLE)

    table = Table([[para]], colWidths=[450])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8D6")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E3C95B")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    
    return table

def create_ai_insight_box(text):
    icon = Image(
        "assets/bulb.png",
        width=0.22 * inch,
        height=0.22* inch,
    )
    title = Paragraph("<b>AI Insight</b>", SUBHEADING_STYLE)
    header = Table([[icon, title]], colWidths=[0.28 * inch, 6.0 * inch])
    header.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
    )

    body = Paragraph(text, BODY_STYLE)
    table = Table(
        [
            [header],
            [body],
        ],
        colWidths=[450],
    )

    table.setStyle(
        TableStyle(
            [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF7FF")),
            ("LINEBEFORE", (0, 0), (0, -1), 5, colors.HexColor("#2F80ED")),
            ("BOX", (0, 0), (-1, -1), 5, colors.HexColor("#B8D8F5")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
    ))
    
    return table


def draw_header_footer(canvas, doc):
    """
    Draw corporate header and footer.
    """

    canvas.saveState()

    page_width, page_height = doc.pagesize

    # Header

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        canvas.drawImage(
            ImageReader(logo_path),
            doc.leftMargin,
            page_height - 72,
            width=0.80 * inch,
            height=0.80 * inch,
            preserveAspectRatio=True,
            mask="auto",
        )

    text_x = doc.leftMargin + 0.95 * inch

    canvas.setFillColor(PRIMARY)
    canvas.setFont("Helvetica-Bold", 18)

    canvas.drawString(
        text_x,
        page_height - 38,
        "ABC Analytics Pvt Ltd",
    )

    canvas.setFillColor(SUBTEXT)
    canvas.setFont("Helvetica", 10)

    canvas.drawString(
        text_x,
        page_height - 58,
        "Data Driven Decision with AI",
    )

    canvas.setStrokeColor(colors.black)

    canvas.line(
        doc.leftMargin,
        page_height - 82,
        page_width - doc.rightMargin,
        page_height - 82,
    )

    # Footer

    canvas.line(
        doc.leftMargin,
        32,
        page_width - doc.rightMargin,
        32,
    )

    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(TEXT)

    canvas.drawString(
        doc.leftMargin,
        14,
        "ABC Analytics Pvt Ltd",
    )

    canvas.drawCentredString(
        page_width / 2,
        14,
        "Confidential",
    )

    canvas.drawRightString(
        page_width - doc.rightMargin,
        14,
        f"Page {canvas.getPageNumber()}",
    )

    canvas.restoreState()