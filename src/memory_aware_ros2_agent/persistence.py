"""Persistence interfaces for memory-aware ROS2 data."""

from __future__ import annotations

from typing import Protocol

from memory_aware_ros2_agent.models import MemoryEvent, RecallResult, TaskTrace


class MemoryStore(Protocol):
    """Storage contract for memory events and task traces."""

    def save_event(self, event: MemoryEvent) -> None:
        """Persist or replace a memory event."""

    def get_event(self, event_id: str) -> MemoryEvent | None:
        """Return a memory event by id, if present."""

    def list_events(self, trace_id: str | None = None) -> tuple[MemoryEvent, ...]:
        """Return persisted events, optionally filtered by trace id."""

    def delete_event(self, event_id: str) -> None:
        """Delete a memory event by id if present."""

    def save_trace(self, trace: TaskTrace) -> None:
        """Persist or replace a task trace."""

    def get_trace(self, trace_id: str) -> TaskTrace | None:
        """Return a task trace by id, if present."""

    def list_traces(self) -> tuple[TaskTrace, ...]:
        """Return persisted task traces."""

    def delete_trace(self, trace_id: str) -> None:
        """Delete a task trace by id if present."""

    def save_recall_result(self, result: RecallResult) -> None:
        """Persist or replace a recall result."""

    def get_recall_result(self, query_id: str) -> RecallResult | None:
        """Return a recall result by query id, if present."""

    def list_recall_results(self) -> tuple[RecallResult, ...]:
        """Return persisted recall results."""

    def delete_recall_result(self, query_id: str) -> None:
        """Delete a recall result by query id if present."""

    def close(self) -> None:
        """Release backend resources."""
