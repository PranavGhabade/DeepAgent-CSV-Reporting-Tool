"""
Task Manager

Responsible for:
1. Maintaining the task queue
2. Assigning tasks to agents
3. Executing tasks
"""

from __future__ import annotations

from typing import Dict, List, Optional

from agents.profiler import ProfilerAgent
from agents.statistics import StatisticsAgent
from agents.visualization import VisualizationAgent
from agents.business_insight import BusinessInsightAgent
from agents.report import ReportAgent
from memory.memory_store import MemoryStore
from models.task import Task, TaskStatus, TaskType


class TaskManager:

    def __init__(self, memory: MemoryStore):

        self.memory = memory

        self.tasks: List[Task] = []

        self.agent_registry: Dict[TaskType, object] = {
            TaskType.PROFILE: ProfilerAgent(self.memory),

            # Will be added later
            TaskType.CLEANING: None,
            TaskType.STATISTICS: StatisticsAgent(self.memory),
            TaskType.VISUALIZATION: VisualizationAgent(self.memory),
            TaskType.BUSINESS_INSIGHT: BusinessInsightAgent(self.memory),
            TaskType.REPORT: ReportAgent(self.memory),
            TaskType.EXPORT: None,
            TaskType.GENERAL: None,
        }

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_next_task(self) -> Optional[Task]:

        pending = [
            task
            for task in self.tasks
            if task.status == TaskStatus.PENDING
        ]

        if not pending:
            return None

        pending.sort(key=lambda x: x.priority)

        return pending[0]

    def execute_task(self, task: Task):

        agent = self.agent_registry.get(task.type)

        if agent is None:
            raise NotImplementedError(
                f"No agent implemented for {task.type.value}"
            )

        task.assign(agent.__class__.__name__)

        return agent.run(task)

    def pending_tasks(self):
        return [
            t for t in self.tasks
            if t.status == TaskStatus.PENDING
        ]

    def running_tasks(self):
        return [
            t for t in self.tasks
            if t.status == TaskStatus.RUNNING
        ]

    def completed_tasks(self):
        return [
            t for t in self.tasks
            if t.status == TaskStatus.COMPLETED
        ]

    def failed_tasks(self):
        return [
            t for t in self.tasks
            if t.status == TaskStatus.FAILED
        ]

    def clear(self):
        self.tasks.clear()