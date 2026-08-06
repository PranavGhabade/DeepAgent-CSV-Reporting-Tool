"""
Dataset Overview Renderer

Responsible ONLY for rendering the Dataset Overview section.
"""

from reportlab.platypus import Spacer
from reportlab.lib.units import inch

from utils.pdf_generator.pdf_components import (
    create_section_header,
    create_kpi_cards,
    create_narrative,
    create_styled_table,
)

from utils.pdf_generator.helpers import (
    is_table_line,
    parse_markdown_table,
)


def render_dataset_overview(
    overview_lines,
    dataset_info,
):
    """
    Render Dataset Overview section.

    Parameters
    ----------
    overview_lines : list[str]

    dataset_info : dict

    Returns
    -------
    list
        ReportLab story elements.
    """

    story = []

    # Normalize dataset information
    dataset = dataset_info.get("dataset_info", dataset_info)

    # -----------------------------------------
    # Section Heading
    # -----------------------------------------

    story.append(
        create_section_header("Dataset Overview")
    )

    # -----------------------------------------
    # KPI Cards
    # -----------------------------------------

    rows = dataset.get("rows", "---")

    columns = dataset.get("columns", "---")

    duplicates = dataset.get(
        "duplicate_rows",
        dataset.get("duplicates_rows", "---"),
    )

    missing = dataset.get(
        "missing_values",
        dataset.get("missing", "0"),
    )

    kpis = [

    (f"{rows:,}" if isinstance(rows, int) else str(rows), "Rows"),

    (str(columns), "Columns"),

    (str(missing), "Missing"),

    (f"{duplicates:,}" if isinstance(duplicates, int) else str(duplicates),"Duplicates"),
    ]

    story.append(
        create_kpi_cards(kpis)
    )

    story.append(
        Spacer(1, 0.25 * inch)
    )

    # -----------------------------------------
    # Render Markdown
    # -----------------------------------------

    table_buffer = []

    for line in overview_lines:

        if is_table_line(line):

            table_buffer.append(line)

            continue

        if table_buffer:

            table = parse_markdown_table(table_buffer)

            story.append(
                create_styled_table(table)
            )

            story.append(
                Spacer(1, 0.20 * inch)
            )

            table_buffer.clear()

        if line.strip():

            lower = line.lower()

            if (
                "number of rows" in lower
                or "number of columns" in lower
            ):
                continue

            story.append(
                create_narrative(line)
            )

            story.append(
                Spacer(1, 0.08 * inch)
            )

    # Flush final table

    if table_buffer:

        table = parse_markdown_table(table_buffer)

        story.append(
            create_styled_table(table)
        )

    return story