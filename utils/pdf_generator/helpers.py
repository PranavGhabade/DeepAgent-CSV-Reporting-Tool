"""
PDF Helper Functions

Reusable utility functions used by the PDF generators.
"""

from __future__ import annotations

import re


def is_heading(line: str) -> bool:
    """Return True if the line is a markdown heading."""

    return line.startswith("### ")


def get_heading_text(line: str) -> str:
    """Remove markdown heading prefix."""

    return line.replace("### ", "").strip()


def is_table_line(line: str) -> bool:
    """Return True if the line belongs to a markdown table."""

    return "|" in line

def is_table(line: str) -> bool:
    """
    Return True if the line is part of a markdown table.
    """

    return line.strip().startswith("|")


def is_bullet(line: str) -> bool:
    """Detect markdown bullet."""

    line = line.strip()

    return (
        line.startswith("- ")
        or line.startswith("* ")
        or bool(re.match(r"^\d+\.", line))
    )


def strip_bullet(line: str) -> str:
    """Remove bullet markers."""

    line = line.strip()

    line = re.sub(r"^\d+\.\s*", "", line)
    line = re.sub(r"^[-*]\s*", "", line)

    return line.strip()


def clean_inline_markdown(text: str) -> str:
    """
    Remove inline markdown symbols.
    """

    text = text.replace("**", "")
    text = text.replace("*", "")
    text = text.replace("`", "")

    return text.strip()


def parse_markdown_table(lines):
    """
    Convert markdown table lines into
    a list of rows.

    Returns
    -------
    [
        ["A","B"],
        ["1","2"]
    ]
    """

    table = []

    for line in lines:

        if "---" in line:
            continue

        cells = [
            clean_inline_markdown(cell)
            for cell in line.split("|")
            if cell.strip()
        ]

        if cells:
            table.append(cells)

    return table