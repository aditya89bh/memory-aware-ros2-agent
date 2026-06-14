"""Autonomous navigation task trace example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.factories import create_memory_event, create_task_trace
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.serialization import model_to_dict


def build_trace() -> dict[str, object]:
    trace_id = "trace-navigation-demo"
    events = (
        create_memory_event(
            trace_id=trace_id,
            event_id="nav-started",
            event_type=EventType.TASK_STARTED,
            timestamp="2026-06-14T12:00:00Z",
            summary="Navigation task started from staging.",
            payload={"start": "staging", "goal": "dock-3"},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="nav-obstacle-observed",
            event_type=EventType.TASK_OBSERVED,
            timestamp="2026-06-14T12:00:07Z",
            summary="Temporary obstacle detected near aisle marker A4.",
            payload={"obstacle": "cart", "distance_meters": 1.8},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="nav-reroute-decided",
            event_type=EventType.TASK_DECIDED,
            timestamp="2026-06-14T12:00:09Z",
            summary="Rerouted through aisle B to preserve clearance.",
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="nav-reroute-acted",
            event_type=EventType.TASK_ACTED,
            timestamp="2026-06-14T12:00:20Z",
            summary="Robot followed alternate route to dock.",
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="nav-succeeded",
            event_type=EventType.TASK_SUCCEEDED,
            timestamp="2026-06-14T12:00:35Z",
            summary="Robot reached dock-3.",
        ),
    )
    return model_to_dict(
        create_task_trace(
            trace_id=trace_id,
            task_name="navigation",
            started_at="2026-06-14T12:00:00Z",
            events=events,
            ended_at="2026-06-14T12:00:35Z",
        )
    )


def main() -> None:
    print(json.dumps(build_trace(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
