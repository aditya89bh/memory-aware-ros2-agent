"""Pick-and-place task trace example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.factories import create_memory_event, create_task_trace
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.serialization import model_to_dict


def build_trace() -> dict[str, object]:
    trace_id = "trace-pick-place-demo"
    events = (
        create_memory_event(
            trace_id=trace_id,
            event_id="pick-place-started",
            event_type=EventType.TASK_STARTED,
            timestamp="2026-06-14T10:00:00Z",
            summary="Pick-and-place task started.",
            payload={"source_bin": "bin-a", "target_fixture": "fixture-1"},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="pick-place-observed",
            event_type=EventType.TASK_OBSERVED,
            timestamp="2026-06-14T10:00:02Z",
            summary="Part pose detected with high confidence.",
            payload={"confidence": 0.97},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="pick-place-acted",
            event_type=EventType.TASK_ACTED,
            timestamp="2026-06-14T10:00:08Z",
            summary="Robot placed part into target fixture.",
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="pick-place-succeeded",
            event_type=EventType.TASK_SUCCEEDED,
            timestamp="2026-06-14T10:00:10Z",
            summary="Pick-and-place task completed.",
            payload={"cycle_time_seconds": 10},
        ),
    )
    trace = create_task_trace(
        trace_id=trace_id,
        task_name="pick-and-place",
        started_at="2026-06-14T10:00:00Z",
        events=events,
        ended_at="2026-06-14T10:00:10Z",
    )
    return model_to_dict(trace)


def main() -> None:
    print(json.dumps(build_trace(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
