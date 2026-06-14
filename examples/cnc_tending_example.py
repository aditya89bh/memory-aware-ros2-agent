"""CNC tending task trace example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.factories import create_memory_event, create_task_trace
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.serialization import model_to_dict


def build_trace() -> dict[str, object]:
    trace_id = "trace-cnc-tending-demo"
    events = (
        create_memory_event(
            trace_id=trace_id,
            event_id="cnc-load-started",
            event_type=EventType.TASK_STARTED,
            timestamp="2026-06-14T11:00:00Z",
            summary="CNC tending task started.",
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="cnc-door-observed",
            event_type=EventType.TASK_OBSERVED,
            timestamp="2026-06-14T11:00:03Z",
            summary="Machine door open and chuck ready.",
            payload={"machine": "cnc-01", "door_open": True},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="cnc-part-loaded",
            event_type=EventType.TASK_ACTED,
            timestamp="2026-06-14T11:00:15Z",
            summary="Raw part loaded into chuck.",
            payload={"grip_force_newtons": 42},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="cnc-cycle-observed",
            event_type=EventType.TASK_OBSERVED,
            timestamp="2026-06-14T11:02:30Z",
            summary="Machining cycle completed normally.",
            payload={"cycle_status": "complete"},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="cnc-tending-succeeded",
            event_type=EventType.TASK_SUCCEEDED,
            timestamp="2026-06-14T11:02:45Z",
            summary="Finished part unloaded and staged.",
        ),
    )
    return model_to_dict(
        create_task_trace(
            trace_id=trace_id,
            task_name="cnc-tending",
            started_at="2026-06-14T11:00:00Z",
            events=events,
            ended_at="2026-06-14T11:02:45Z",
        )
    )


def main() -> None:
    print(json.dumps(build_trace(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
