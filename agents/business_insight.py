"""
Business Insight Agent

Uses Gemini to interpret the outputs produced by other agents
and generate business-oriented insights.
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from llm.gemini import llm
from memory.memory_store import MemoryStore
from models.task import Task
from prompts.business_insight_prompt import BUSINESS_INSIGHT_PROMPT


class BusinessInsightAgent(BaseAgent):

    def __init__(self, memory: MemoryStore):
        super().__init__(memory)

    def execute(self, task: Task):

        print("\n===== BUSINESS INSIGHT AGENT =====")

        context = self.memory.business_insight_context()

        prompt = BUSINESS_INSIGHT_PROMPT.format(
            profile=context["profile"] or "Dataset profile unavailable.",
            statistics=context["statistics"] or "No statistical analysis available.",
            visualizations=context["visualizations"] or "No visualizations available.",
            query=self.memory.latest_user_query(),
        )

        print("\nGenerating business insights...")

        response = llm.invoke(prompt)

        insights = response.content

        if isinstance(insights, list):
            insights = insights[0]["text"]

        insights = insights.strip()

        if not insights:
            insights = (
                "No business insights could be generated from the available analysis."
            )

        self.memory.store_analysis(
            "business_insights",
            insights,
        )

        self.memory.add_history(
            "assistant",
            insights,
        )

        print("BusinessInsightAgent completed successfully.")

        return insights