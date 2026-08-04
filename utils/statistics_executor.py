"""
Statistics Executor

Executes the statistical operations selected by the StatisticsAgent.
"""

from __future__ import annotations

from tools.statistics_tool import StatisticsTool


class StatisticsExecutor:
    """
    Executes statistical operations returned by the LLM.
    """

    OPERATION_MAP = {
        "basic_info": StatisticsTool.basic_info,
        "column_types": StatisticsTool.column_types,
        "missing_values": StatisticsTool.missing_values,
        "summary_statistics": StatisticsTool.summary_statistics,
        "numeric_statistics": StatisticsTool.numeric_statistics,
        "correlation_matrix": StatisticsTool.correlation_matrix,
        "top_categories": StatisticsTool.top_categories,
        "outliers": StatisticsTool.detect_outliers,
    }

    @classmethod
    def execute(cls, df, operations):

        results = {}

        for operation in operations:

            operation_name = operation.get("operation")

            print(f"\nExecuting statistics -> {operation_name}")

            # Simple operations
            if operation_name in cls.OPERATION_MAP:

                results[operation_name] = cls.OPERATION_MAP[
                    operation_name
                ](df)

            # Group By
            elif operation_name == "group_by":

                results["group_by"] = StatisticsTool.group_by(
                    df=df,
                    group_column=operation["group_column"],
                    aggregations=operation["aggregations"],
                )

            # Sort
            elif operation_name == "sort":

                results["sort"] = StatisticsTool.sort(
                    df=df,
                    column=operation["column"],
                    ascending=operation.get("ascending", True),
                )

            # Filter
            elif operation_name == "filter":

                results["filter"] = StatisticsTool.filter_rows(
                    df=df,
                    column=operation["column"],
                    operator=operation["operator"],
                    value=operation["value"],
                )

            # Top N
            elif operation_name == "top_n":

                results["top_n"] = StatisticsTool.top_n(
                    df=df,
                    column=operation["column"],
                    n=operation.get("n", 10),
                )

            else:

                print(f"Unknown statistics operation: {operation_name}")

        return results