"""
Visualization Agent

Uses Gemini to decide which visualizations should be generated,
then delegates chart creation to the VisualizationExecutor.
"""

from __future__ import annotations

import json

from agents.base_agent import BaseAgent
from llm.gemini import llm
from memory.memory_store import MemoryStore
from models.task import Task
from prompts.visualization_prompt import VISUALIZATION_PROMPT
from utils.visualization_executor import VisualizationExecutor


class VisualizationAgent(BaseAgent):

    def __init__(self, memory: MemoryStore):
        super().__init__(memory)

    def execute(self, task: Task):

        print("\n===== VISUALIZATION AGENT =====")

        df = self.memory.get_dataset("dataframe")

        if df is None:
            raise ValueError("Dataframe not found in shared memory.")

        context = self.memory.visualization_context()

        prompt = VISUALIZATION_PROMPT.format(
            profile=context["profile"] or "Dataset not profiled.",
            query=self.memory.latest_user_query(),
        )

        print("\nPlanning visualizations...")

        print("\nUser Query:")
        print(self.memory.latest_user_query())

        print("\nPrompt Preview:")
        print(prompt[-500:])

        response = llm.invoke(prompt)

        # --------------------------------------------------
        # Extract Gemini Response
        # --------------------------------------------------

        raw_response = response.content

        if isinstance(raw_response, list):
            raw_response = raw_response[0]["text"]

        raw_response = str(raw_response).strip()

        # --------------------------------------------------
        # Remove Markdown JSON Fences
        # --------------------------------------------------

        if raw_response.startswith("```json"):
            raw_response = raw_response.replace("```json", "", 1)

        if raw_response.startswith("```"):
            raw_response = raw_response.replace("```", "", 1)

        if raw_response.endswith("```"):
            raw_response = raw_response[:-3]

        raw_response = raw_response.strip()

        print("\nVisualization Plan:")
        print(raw_response)

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            plan = json.loads(raw_response)

            if "visualizations" not in plan:
                raise ValueError("Missing 'visualizations' key.")

            print("\nParsed Visualization Plan:")
            print(json.dumps(plan, indent=4))

        except Exception as e:

            print("\nVisualization JSON Error")
            print(e)

            print("\nUsing fallback visualization plan.")

            numeric_columns = df.select_dtypes(include="number").columns.tolist()
            categorical_columns = df.select_dtypes(include="object").columns.tolist()

            fallback = []

            if numeric_columns:
                fallback.append({
                    "chart": "histogram",
                    "column": numeric_columns[0],
                })

            if len(numeric_columns) >= 2:
                fallback.append({
                    "chart": "scatter",
                    "x": numeric_columns[0],
                    "y": numeric_columns[1],
                })

            if categorical_columns and numeric_columns:
                fallback.append({
                    "chart": "bar",
                    "x": categorical_columns[0],
                    "y": numeric_columns[0],
                })

            if categorical_columns:
                fallback.append({
                    "chart": "pie",
                    "column": categorical_columns[0],
                })

            plan = {
                "visualizations": fallback
            }

        # --------------------------------------------------
        # Execute Charts
        # --------------------------------------------------

        visualizations = plan.get("visualizations", [])

        if not visualizations:

            print("\nNo visualizations requested.")

            self.memory.store_analysis(
                "visualizations",
                {},
            )

            return {}

        print(f"\nGenerating {len(visualizations)} visualization(s)...")

        charts = VisualizationExecutor.execute(
            df,
            visualizations,
        )

        print("\nGenerated Charts:")

        for name, path in charts.items():
            print(f"{name} -> {path}")

        self.memory.store_analysis(
            "visualizations",
            charts,
        )

        return charts