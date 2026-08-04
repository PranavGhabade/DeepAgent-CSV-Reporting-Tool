"""
Visualization Tool

Generates charts from a dataframe.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class VisualizationTool:

    OUTPUT_DIR = Path("outputs/charts")

    @classmethod
    def _prepare_output_dir(cls):
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def resolve_column(df: pd.DataFrame, column: str) -> str:
        """
        Resolve an LLM-generated column name to the closest dataframe column.
        """

        if column in df.columns:
            return column

        normalized = {
            c.lower().replace(" ", "").replace("_", ""): c
            for c in df.columns
        }

        key = column.lower().replace(" ", "").replace("_", "")

        if key in normalized:
            return normalized[key]

        for candidate in normalized:
            if key in candidate or candidate in key:
                return normalized[candidate]

        raise ValueError(
            f"Column '{column}' not found. "
            f"Available columns: {list(df.columns)}"
        )

    @staticmethod
    def safe_filename(name: str) -> str:
        """
        Convert column names into filesystem-safe names.
        """

        return (
            name.replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
                .replace("(", "")
                .replace(")", "")
        )

    # --------------------------------------------------
    # Histogram
    # --------------------------------------------------

    @classmethod
    def histogram(cls, df: pd.DataFrame, column: str):

        cls._prepare_output_dir()

        column = cls.resolve_column(df, column)
        safe_column = cls.safe_filename(column)

        plt.figure(figsize=(8, 5))

        df[column].dropna().hist(bins=20)

        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        output_path = cls.OUTPUT_DIR / f"{safe_column}_histogram.png"

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    # --------------------------------------------------
    # Box Plot
    # --------------------------------------------------

    @classmethod
    def box_plot(cls, df: pd.DataFrame, column: str):

        cls._prepare_output_dir()

        column = cls.resolve_column(df, column)
        safe_column = cls.safe_filename(column)

        plt.figure(figsize=(6, 5))

        df.boxplot(column=column)

        plt.title(f"Box Plot of {column}")

        output_path = cls.OUTPUT_DIR / f"{safe_column}_box.png"

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    # --------------------------------------------------
    # Bar Chart
    # --------------------------------------------------

    @classmethod
    def bar_chart(cls, df: pd.DataFrame, x: str, y: str):

        cls._prepare_output_dir()

        x = cls.resolve_column(df, x)
        y = cls.resolve_column(df, y)

        safe_x = cls.safe_filename(x)
        safe_y = cls.safe_filename(y)

        data = (
            df.groupby(x)[y]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(10, 5))

        data.plot(kind="bar")

        plt.title(f"{y} by {x}")
        plt.xlabel(x)
        plt.ylabel(y)

        output_path = cls.OUTPUT_DIR / f"{safe_x}_{safe_y}_bar.png"

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    # --------------------------------------------------
    # Line Chart
    # --------------------------------------------------

    @classmethod
    def line_chart(cls, df: pd.DataFrame, x: str, y: str):

        cls._prepare_output_dir()

        x = cls.resolve_column(df, x)
        y = cls.resolve_column(df, y)

        safe_x = cls.safe_filename(x)
        safe_y = cls.safe_filename(y)

        data = (
            df.groupby(x)[y]
            .sum()
            .sort_index()
        )

        plt.figure(figsize=(10, 5))

        data.plot(kind="line", marker="o")

        plt.title(f"{y} by {x}")
        plt.xlabel(x)
        plt.ylabel(y)

        output_path = cls.OUTPUT_DIR / f"{safe_x}_{safe_y}_line.png"

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    # --------------------------------------------------
    # Scatter Plot
    # --------------------------------------------------

    @classmethod
    def scatter_plot(cls, df: pd.DataFrame, x: str, y: str):

        cls._prepare_output_dir()

        x = cls.resolve_column(df, x)
        y = cls.resolve_column(df, y)

        safe_x = cls.safe_filename(x)
        safe_y = cls.safe_filename(y)

        plt.figure(figsize=(8, 6))

        plt.scatter(df[x], df[y])

        plt.title(f"{y} vs {x}")
        plt.xlabel(x)
        plt.ylabel(y)

        output_path = cls.OUTPUT_DIR / f"{safe_x}_{safe_y}_scatter.png"

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    # --------------------------------------------------
    # Pie Chart
    # --------------------------------------------------

    @classmethod
    def pie_chart(cls, df: pd.DataFrame, column: str):

        cls._prepare_output_dir()

        column = cls.resolve_column(df, column)
        safe_column = cls.safe_filename(column)

        counts = df[column].value_counts().head(10)

        plt.figure(figsize=(8, 8))

        counts.plot(
            kind="pie",
            autopct="%1.1f%%"
        )

        plt.ylabel("")
        plt.title(f"{column} Distribution")

        output_path = cls.OUTPUT_DIR / f"{safe_column}_pie.png"

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)