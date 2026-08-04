from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

styles = getSampleStyleSheet()

# Corporate color palette
PRIMARY = colors.HexColor("#1F4E79")
SECONDARY = colors.HexColor("#5B9BD5")
ACCENT = colors.HexColor("#ED7D31")
SUCCESS = colors.HexColor("#70AD47")
WARNING = colors.HexColor("#FFC000")

TEXT = colors.HexColor("#222222")
SUBTEXT = colors.HexColor("#666666")

LIGHT_BG = colors.HexColor("#F5F7FA")
TABLE_HEADER = colors.HexColor("#D9EAF7")
BORDER = colors.HexColor("#D0D7DE")

# Title
TITLE_STYLE = ParagraphStyle(
    "ReportTitle",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
    fontSize=24,
    textColor=PRIMARY,
    spaceBefore=6,
    spaceAfter=18,
)

# Main heading
HEADING_STYLE = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=18,
    textColor=PRIMARY,
    alignment=TA_LEFT,
    spaceBefore=14,
    spaceAfter=8,
    leftIndent=0,
    firstLineIndent=0,
)

# Subheading
SUBHEADING_STYLE = ParagraphStyle(
    "SubHeading",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=14,
    textColor=PRIMARY,
    spaceBefore=10,
    spaceAfter=6,
)

# Figure caption
CAPTION_STYLE = ParagraphStyle(
    "Caption",
    parent=styles["BodyText"],
    fontName="Helvetica-Oblique",
    fontSize=10,
    alignment=TA_CENTER,
    textColor=SUBTEXT,
    spaceBefore=4,
    spaceAfter=10,
)

# Body
BODY_STYLE = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=16,
    textColor=TEXT,
    alignment=TA_LEFT,
    spaceAfter=8,
)

HIGHLIGHT_STYLE = ParagraphStyle(
    "Points",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=16,
    textColor=TEXT,
    alignment=TA_LEFT,
    spaceAfter=0,
)
# Bullet
BULLET_STYLE = ParagraphStyle(
    "Bullet",
    parent=BODY_STYLE,
    leftIndent=18,
    firstLineIndent=-8,
    leading=16,
    spaceBefore=2,
    spaceAfter=2,
)

# AI insight box
INSIGHT_STYLE = ParagraphStyle(
    "Insight",
    parent=BODY_STYLE,
    backColor=LIGHT_BG,
    borderColor=SECONDARY,
    borderWidth=1,
    borderPadding=10,
    borderRadius=10,
    spaceBefore=8,
    spaceAfter=10,
)

# Footer
FOOTER_STYLE = ParagraphStyle(
    "Footer",
    parent=BODY_STYLE,
    fontSize=8,
    textColor=SUBTEXT,
    alignment=TA_CENTER,
)
