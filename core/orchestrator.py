"""
Deep Agent Orchestrator

Coordinates the entire workflow.

Responsibilities:
1. Receive user requests
2. Maintain shared state
3. Interact with Task Manager
4. Manage shared memory
"""

from __future__ import annotations

from models.state import AgentState
from core.task_manager import TaskManager
from memory.memory_store import MemoryStore
from agents.planner import PlannerAgent


class Orchestrator:
    """Central controller of the Deep Agent system."""

    def __init__(self):
        self.state = AgentState()
        self.memory = MemoryStore()
        self.planner = PlannerAgent(self.memory)
        self.task_manager = TaskManager(self.memory)

    # Dataset

    def set_dataset(self, csv_path: str):
        """Register the uploaded dataset."""
        self.state.csv_path = csv_path
        self.memory.store_dataset("path", csv_path)

    # Conversation

    def receive_user_query(self, query: str):
        """
        Store the latest user query in shared memory.
        """

        self.memory.add_history(
            role="user",
            message=query,
        )

    # Task Management

    def add_task(self, task):
        self.task_manager.add_task(task)
        self.state.add_task(task)

    def get_next_task(self):
        return self.task_manager.get_next_task()

    def assign_task(self, task):
        return self.task_manager.assign_task(task)

    # Shared Memory

    def store_result(self, key, value):
        self.memory.store(key, value)

    def get_result(self, key):
        return self.memory.retrieve(key)

    def get_chat_history(self):
        return self.memory.get_history()

    # Reset

    def reset(self):
        """
        Clears task queue only.

        Dataset, profile and previous analysis remain
        available for future queries.
        """

        self.task_manager.clear()
        self.state.clear()

    # Planning

    def create_plan(self):

        tasks = self.planner.run(
            self.memory.latest_user_query()
        )

        for task in tasks:
            self.add_task(task)

        return tasks

    # Execution

    def execute_next_task(self):

        task = self.task_manager.get_next_task()

        if task is None:
            print("No pending tasks.")
            return None

        result = self.task_manager.execute_task(task)

        self.state.complete_task(task)

        return result

    def execute_all_tasks(self):

        results = []

        while True:

            task = self.task_manager.get_next_task()

            if task is None:
                break

            print(f"\nExecuting -> {task.type.value}")

            result = self.execute_next_task()

            results.append(result)

        return results

    # Main Pipeline

    def run(self, user_query: str):

        self.receive_user_query(user_query)

        self.create_plan()

        return self.execute_all_tasks()

    # Public API

    def generate_report(self):
        """
        Execute the complete reporting pipeline.
        """

        report_query = (
            "Generate a complete analytical report for this dataset "
            "including summary statistics, visualizations and business insights."
        )

        self.run(report_query)

        return self.memory.get_report("markdown")

    def answer_query(self, query: str):
        """
        Execute only the agents required to answer
        the user's question.
        """

        results = self.run(query)

        # Priority of returned answer

        if self.memory.get_report("markdown"):
            return self.memory.get_report("markdown")

        if self.memory.get_analysis("business_insights"):
            return self.memory.get_analysis("business_insights")

        if self.memory.get_analysis("statistics"):
            return self.memory.get_analysis("statistics")

        if self.memory.get_analysis("visualizations"):
            return self.memory.get_analysis("visualizations")

        return results