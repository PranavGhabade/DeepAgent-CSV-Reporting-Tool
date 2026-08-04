"""
Task model for the Deep Agent Reporting Tool.

Every user request is broken into one or more Tasks by the Planner Agent.
These tasks are executed by specialized agents through the Task Manager.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class TaskStatus(str, Enum):
    """Lifecycle states of a task."""

    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskType(str, Enum):
    """Supported task categories."""

    PROFILE = "profile"
    CLEANING = "cleaning"
    STATISTICS = "statistics"
    VISUALIZATION = "visualization"
    BUSINESS_INSIGHT = "business_insight"
    REPORT = "report"
    EXPORT = "export"
    GENERAL = "general"


@dataclass
class Task:
    """
    Represents a single unit of work.

    Example:
        Task(
            type=TaskType.STATISTICS,
            description="Calculate total sales by month"
        )
    """

    type: TaskType
    description: str

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1

    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Optional[Any] = None

    assigned_agent: Optional[str] = None
    error: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def assign(self, agent_name: str) -> None:
        """Assign the task to an agent."""
        self.assigned_agent = agent_name
        self.status = TaskStatus.ASSIGNED

    def start(self) -> None:
        """Mark the task as running."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now()

    def complete(self, result: Any = None) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.output_data = result
        self.completed_at = datetime.now()

    def fail(self, error_message: str) -> None:
        """Mark the task as failed."""
        self.status = TaskStatus.FAILED
        self.error = error_message
        self.completed_at = datetime.now()

    def reset(self) -> None:
        """Reset the task for retry."""
        self.status = TaskStatus.PENDING
        self.assigned_agent = None
        self.started_at = None
        self.completed_at = None
        self.output_data = None
        self.error = None

    @property
    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.status == TaskStatus.FAILED

    @property
    def is_running(self) -> bool:
        return self.status == TaskStatus.RUNNING

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to a serializable dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority,
            "assigned_agent": self.assigned_agent,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return (
            f"Task("
            f"id='{self.id[:8]}...', "
            f"type='{self.type.value}', "
            f"status='{self.status.value}', "
            f"description='{self.description}')"
        )