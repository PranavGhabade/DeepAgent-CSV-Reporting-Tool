"""
Report Agent

Uses Gemini to generate a comprehensive Markdown report
from the outputs of previous agents.
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from llm.gemini import llm
from memory.memory_store import MemoryStore
from models.task import Task
from prompts.reporter_prompt import REPORTER_PROMPT
from utils.pdf_report_generator import generate_pdf_report


class ReportAgent(BaseAgent):

    def __init__(self, memory: MemoryStore):
        super().__init__(memory)

    def execute(self, task: Task):

        print("\n===== REPORT AGENT =====")

        context = self.memory.report_context()

        prompt = REPORTER_PROMPT.format(
            profile=context["profile"] or "No dataset profile available.",
            statistics=context["statistics"] or "No statistical analysis available.",
            visualizations=context["visualizations"] or "No visualizations generated.",
            business_insights=context["business_insights"] or "No business insights available.",
            query=self.memory.latest_user_query(),
        )

        print("\nGenerating report...")
        print("\nUser Query:")
        print(self.memory.latest_user_query())

        response = llm.invoke(prompt)

        report = response.content

        if isinstance(report, list):
            report = report[0]["text"]

        report = report.strip()

        # Remove markdown fences if the model returns them
        if report.startswith("```markdown"):
            report = report.replace("```markdown", "", 1)

        if report.startswith("```"):
            report = report.replace("```", "", 1)

        if report.endswith("```"):
            report = report[:-3]

        report = report.strip()

        self.memory.store_report(
            "markdown",
            report,
        )

        pdf_path = generate_pdf_report(self.memory)

        self.memory.store_report(
            "pdf",
            pdf_path,
        )

        print("ReportAgent completed successfully.")

        return {
            "markdown": report,
            "pdf": pdf_path,
        }