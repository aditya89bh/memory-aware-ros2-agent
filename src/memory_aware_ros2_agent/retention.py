"""Retention policy support for persistence stores."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetentionPolicy:
    """Limits for retained persistence records."""

    max_events: int | None = None
    max_traces: int | None = None
    max_recall_results: int | None = None

    def __post_init__(self) -> None:
        for field_name in ("max_events", "max_traces", "max_recall_results"):
            value = getattr(self, field_name)
            if value is not None and value < 0:
                msg = f"{field_name} must be non-negative"
                raise ValueError(msg)


def keep_newest_count(total_count: int, max_count: int | None) -> int:
    """Return how many oldest records should be pruned."""

    if max_count is None:
        return 0
    return max(0, total_count - max_count)
