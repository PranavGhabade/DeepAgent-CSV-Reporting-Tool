"""
Statistics Tool

Pure deterministic functions.
No agent logic.
No memory.
No orchestration.
"""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd


class StatisticsTool:

    # Column Resolver

    @staticmethod
    def resolve_column(df: pd.DataFrame, requested_column: str) -> str:
        """
        Resolve an LLM-generated column name to an actual dataframe column.

        Matching strategy:
        1. Exact match
        2. Case-insensitive match
        3. Ignore spaces and underscores
        4. Partial substring match
        """

        columns = list(df.columns)

        # Exact match
        if requested_column in columns:
            return requested_column

        requested = (
            requested_column.lower()
            .replace("_", "")
            .replace(" ", "")
        )

        # Case-insensitive / normalized
        for column in columns:

            normalized = (
                column.lower()
                .replace("_", "")
                .replace(" ", "")
            )

            if normalized == requested:
                return column

        # Partial match
        for column in columns:

            normalized = (
                column.lower()
                .replace("_", "")
                .replace(" ", "")
            )

            if requested in normalized or normalized in requested:
                return column

        raise ValueError(
            f"Column '{requested_column}' not found.\n"
            f"Available columns:\n{columns}"
        )

    # Dataset Information

    @staticmethod
    def basic_info(df: pd.DataFrame) -> Dict[str, Any]:

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": float(
                round(
                    df.memory_usage(deep=True).sum() / (1024 * 1024),
                    2,
                )
            ),
        }

    # Column Types

    @staticmethod
    def column_types(df: pd.DataFrame):

        return {
            "numeric": df.select_dtypes(include="number").columns.tolist(),
            "categorical": df.select_dtypes(include="object").columns.tolist(),
            "datetime": df.select_dtypes(include="datetime").columns.tolist(),
            "boolean": df.select_dtypes(include="bool").columns.tolist(),
        }

    # Missing Values

    @staticmethod
    def missing_values(df: pd.DataFrame):

        return {
            "count": df.isnull().sum().to_dict(),
            "percentage": (
                (df.isnull().sum() / len(df)) * 100
            ).round(2).to_dict(),
        }

    # Summary Statistics

    @staticmethod
    def summary_statistics(df: pd.DataFrame):

        return (
            df.describe(include="all")
            .fillna("")
            .to_dict()
        )

    # Correlation Matrix

    @staticmethod
    def correlation_matrix(df: pd.DataFrame):

        numeric = df.select_dtypes(include="number")

        if len(numeric.columns) < 2:
            return {}

        return (
            numeric
            .corr()
            .round(3)
            .to_dict()
        )

    # Top Categories

    @staticmethod
    def top_categories(df: pd.DataFrame):

        result = {}

        for column in df.select_dtypes(include="object"):

            result[column] = (
                df[column]
                .value_counts(dropna=False)
                .head(5)
                .to_dict()
            )

        return result

    # Numeric Statistics

    @staticmethod
    def numeric_statistics(df: pd.DataFrame):

        result = {}

        for column in df.select_dtypes(include="number"):

            result[column] = {
                "mean": float(df[column].mean()),
                "median": float(df[column].median()),
                "std": float(df[column].std()),
                "min": float(df[column].min()),
                "max": float(df[column].max()),
            }

        return result

    # Outlier Detection

    @staticmethod
    def detect_outliers(df: pd.DataFrame):

        result = {}

        for column in df.select_dtypes(include="number"):

            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)

            result[column] = int(
                ((df[column] < lower) |
                 (df[column] > upper)).sum()
            )

        return result

    # Group By

    @staticmethod
    def group_by(
        df: pd.DataFrame,
        group_column: str,
        aggregations: dict,
    ):

        group_column = StatisticsTool.resolve_column(
            df,
            group_column,
        )

        resolved_aggregations = {}

        for column, agg in aggregations.items():

            resolved_column = StatisticsTool.resolve_column(
                df,
                column,
            )

            resolved_aggregations[resolved_column] = agg

        result = (
            df.groupby(group_column)
            .agg(resolved_aggregations)
            .reset_index()
        )

        return result.to_dict(orient="records")

    # Filter Rows

    @staticmethod
    def filter_rows(
        df: pd.DataFrame,
        column: str,
        operator: str,
        value,
    ):

        column = StatisticsTool.resolve_column(
            df,
            column,
        )

        operators = {
            ">": df[column] > value,
            "<": df[column] < value,
            ">=": df[column] >= value,
            "<=": df[column] <= value,
            "==": df[column] == value,
            "!=": df[column] != value,
        }

        if operator not in operators:
            raise ValueError(f"Unsupported operator: {operator}")

        result = df[operators[operator]]

        return result.to_dict(orient="records")

    # Sort

    @staticmethod
    def sort(
        df: pd.DataFrame,
        column: str,
        ascending: bool = True,
    ):

        column = StatisticsTool.resolve_column(
            df,
            column,
        )

        result = df.sort_values(
            by=column,
            ascending=ascending,
        )

        return result.to_dict(orient="records")

    # Top N


    @staticmethod
    def top_n(
        df: pd.DataFrame,
        column: str,
        n: int = 10,
    ):

        column = StatisticsTool.resolve_column(
            df,
            column,
        )

        result = (
            df.sort_values(
                by=column,
                ascending=False,
            )
            .head(n)
        )

        return result.to_dict(orient="records")