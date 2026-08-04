"""
Planner Agent

Responsible for converting a user request into executable Tasks.

The planner decides WHAT should be done,
not HOW it should be done.
"""

from __future__ import annotations

import json
from typing import List

from llm.gemini import llm
from memory.memory_store import MemoryStore
from models.task import Task, TaskType
from prompts.planner_prompt import PLANNER_PROMPT


class PlannerAgent:

    def __init__(self, memory: MemoryStore):
        self.memory = memory

        self.task_mapping = {
            "PROFILE": TaskType.PROFILE,
            "STATISTICS": TaskType.STATISTICS,
            "VISUALIZATION": TaskType.VISUALIZATION,
            "BUSINESS_INSIGHT": TaskType.BUSINESS_INSIGHT,
            "REPORT": TaskType.REPORT,
            "CLEANING": TaskType.CLEANING,
            "EXPORT": TaskType.EXPORT,
        }

    def run(self, user_query: str) -> List[Task]:

        print("\n===== PLANNER AGENT =====")

        # Get planner context from memory
        context = self.memory.planner_context()

        prompt = PLANNER_PROMPT.format(
            profile=context["profile"] or "Dataset has not been profiled yet.",
            available_analysis=context["available_analysis"],
            history=context["history"] or "No previous conversation.",
            query=user_query,
        )

        response = llm.invoke(prompt)

        # Extract text from Gemini response
        if isinstance(response.content, list):
            response_text = response.content[0]["text"]
        else:
            response_text = response.content

        print("\nPlanner Response:")
        print(response_text)

        # Parse JSON response
        try:
            planner_output = json.loads(response_text)
        except Exception as e:

            print(f"Planner JSON Parsing Failed: {e}")

            return [
                Task(
                    type=TaskType.GENERAL,
                    description=user_query,
                    priority=99,
                )
            ]

        tasks: List[Task] = []

        # Ensure dataset is profiled first
        if (not self.memory.exists("profile") and "PROFILE" not in planner_output.get("agents", [])):
            tasks.append(
                Task(
                    type=TaskType.PROFILE,
                    description="Profile uploaded dataset",
                    priority=1,
                )
            )

        priority = 2

        for agent_name in planner_output.get("agents", []):

            agent_name = agent_name.upper()

            if agent_name not in self.task_mapping:
                continue

            tasks.append(
                Task(
                    type=self.task_mapping[agent_name],
                    description=f"Execute {agent_name}",
                    priority=priority,
                )
            )

            priority += 1

        if len(tasks) == 0:

            tasks.append(
                Task(
                    type=TaskType.GENERAL,
                    description=user_query,
                    priority=99,
                )
            )

        print(f"\nPlanner created {len(tasks)} task(s).")

        for task in tasks:
            print(f" -> {task.type.name}")

        return tasks