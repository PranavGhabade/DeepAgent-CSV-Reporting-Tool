"""
Base Agent

All agents inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from memory.memory_store import MemoryStore
from models.task import Task


class BaseAgent(ABC):

    def __init__(self, memory: MemoryStore):
        self.memory = memory

    @property
    def name(self):
        return self.__class__.__name__

    def run(self, task: Task):

        print(f"\n===== {self.name.upper()} =====")

        task.start()

        try:

            result = self.execute(task)

            task.complete(result)

            print(f"{self.name} completed successfully.")

            return result

        except Exception as e:

            task.fail(str(e))

            print(f"{self.name} failed.")

            raise

    @abstractmethod
    def execute(self, task: Task):
        """
        Every agent implements only this method.
        """
        pass