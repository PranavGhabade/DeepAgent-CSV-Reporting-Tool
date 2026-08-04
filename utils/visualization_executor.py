"""
Visualization Executor

Executes the visualization operations selected by the
VisualizationAgent.
"""

from __future__ import annotations

from tools.visualization_tool import VisualizationTool


class VisualizationExecutor:
    """
    Executes visualization operations returned by the LLM.
    """

    OPERATION_MAP = {
        "bar": VisualizationTool.bar_chart,
        "line": VisualizationTool.line_chart,
        "scatter": VisualizationTool.scatter_plot,
        "histogram": VisualizationTool.histogram,
        "box": VisualizationTool.box_plot,
        "pie": VisualizationTool.pie_chart,
    }

    @classmethod
    def execute(cls, df, visualizations):
        """
        Execute visualization operations.

        Parameters
        ----------
        df : pandas.DataFrame

        visualizations : list
            Visualization plan returned by Gemini.

        Returns
        -------
        dict
            Generated chart paths.
        """

        charts = {}

        if not visualizations:
            print("No visualizations to generate.")
            return charts

        for index, visualization in enumerate(visualizations, start=1):

            chart = visualization.get("chart")

            print("\n----------------------------------------")
            print(f"Visualization {index}")
            print("----------------------------------------")
            print(visualization)

            if chart not in cls.OPERATION_MAP:
                print(f"Unknown visualization type: {chart}")
                continue

            try:

                # ------------------------------------
                # Histogram / Box
                # ------------------------------------

                if chart in ["histogram", "box"]:

                    column = visualization["column"]

                    output = cls.OPERATION_MAP[chart](
                        df,
                        column,
                    )

                    charts[f"{chart}_{column}"] = output

                # ------------------------------------
                # Pie
                # ------------------------------------

                elif chart == "pie":

                    column = visualization["column"]

                    output = cls.OPERATION_MAP[chart](
                        df,
                        column,
                    )

                    charts[f"{chart}_{column}"] = output

                # ------------------------------------
                # Scatter
                # ------------------------------------

                elif chart == "scatter":

                    x = visualization["x"]
                    y = visualization["y"]

                    output = cls.OPERATION_MAP[chart](
                        df,
                        x,
                        y,
                    )

                    charts[f"{chart}_{x}_{y}"] = output

                # ------------------------------------
                # Bar / Line
                # ------------------------------------

                elif chart in ["bar", "line"]:

                    x = visualization["x"]
                    y = visualization["y"]

                    output = cls.OPERATION_MAP[chart](
                        df,
                        x,
                        y,
                    )

                    charts[f"{chart}_{x}_{y}"] = output

                print(f"✓ Generated -> {output}")

            except KeyError as e:

                print(f"Column missing : {e}")

            except ValueError as e:

                print(f"Invalid visualization : {e}")

            except Exception as e:

                print(f"Unexpected Error : {e}")

        print("\n========================================")
        print("Visualization Summary")
        print("========================================")

        if charts:

            for key, value in charts.items():
                print(f"{key} -> {value}")

        else:

            print("No charts generated.")

        return charts