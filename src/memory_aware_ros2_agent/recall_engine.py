"""Recall engine interfaces and helpers."""

from __future__ import annotations

from typing import Protocol

from memory_aware_ros2_agent.models import RecallQuery, RecallResult
from memory_aware_ros2_agent.persistence import MemoryStore


class RecallEngine(Protocol):
    """Contract for retrieving relevant memories from persisted experience."""

    def recall(self, query: RecallQuery, store: MemoryStore) -> RecallResult:
        """Return relevant persisted memories for a query."""
