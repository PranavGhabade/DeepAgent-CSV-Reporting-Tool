"""
Statistics Agent

Uses the LLM to decide which statistical operations should be executed,
then delegates execution to the StatisticsExecutor.
"""

from __future__ import annotations

import json

from agents.base_agent import BaseAgent
from llm.gemini import llm
from memory.memory_store import MemoryStore
from models.task import Task
from prompts.statistics_prompt import STATISTICS_PROMPT
from utils.statistics_executor import StatisticsExecutor


class StatisticsAgent(BaseAgent):

    def __init__(self, memory: MemoryStore):
        super().__init__(memory)

    def _build_prompt(self) -> str:
        """Build the Statistics Agent prompt."""

        context = self.memory.statistics_context()

        return STATISTICS_PROMPT.format(
            profile=context["profile"] or "Dataset not profiled.",
            query=self.memory.latest_user_query(),
        )

    def _extract_response_text(self, response) -> str:
        """Extract only the text returned by Gemini."""

        content = response.content

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            for item in content:

                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text", "").strip()

        raise ValueError("Unable to extract text from Gemini response.")

    def execute(self, task: Task):

        print("\n===== STATISTICS AGENT =====")

        df = self.memory.get_dataset("dataframe")

        if df is None:
            raise ValueError("Dataframe not found in shared memory.")

        prompt = self._build_prompt()

        print("\nPlanning statistical operations...")

        print("\nUser Query:")
        print(self.memory.latest_user_query())

        print("\nPrompt Preview:")
        print(prompt[-500:])


        response = llm.invoke(prompt)

        raw_response = self._extract_response_text(response)

        print("\nStatistics Plan:")
        print(raw_response)

        try:
            plan = json.loads(raw_response)

        except json.JSONDecodeError:

            print("\nInvalid JSON received. Using default statistics plan.")

            plan = {
                "operations": [
                    {
                        "operation": "basic_info"
                    },
                    {
                        "operation": "summary_statistics"
                    }
                ]
            }

        operations = plan.get("operations", [])

        if not operations:

            print("\nNo operations returned. Using default statistics plan.")

            operations = [
                {
                    "operation": "basic_info"
                }
            ]

        statistics = StatisticsExecutor.execute(
            df=df,
            operations=operations,
        )

        self.memory.store_analysis(
            "statistics",
            statistics,
        )

        print("\nStatisticsAgent completed successfully.")

        return statistics