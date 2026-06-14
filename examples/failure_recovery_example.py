"""Failure recovery task trace example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.factories import create_memory_event, create_task_trace
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.serialization import model_to_dict
from memory_aware_ros2_agent.trace_intelligence import summarize_experience


def build_trace_summary() -> dict[str, object]:
    trace_id = "trace-failure-recovery-demo"
    events = (
        create_memory_event(
            trace_id=trace_id,
            event_id="recovery-started",
            event_type=EventType.TASK_STARTED,
            timestamp="2026-06-14T13:00:00Z",
            summary="Docking task started.",
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="recovery-failed",
            event_type=EventType.TASK_FAILED,
            timestamp="2026-06-14T13:00:12Z",
            summary="Docking approach timed out.",
            payload={"reason": "timeout", "retry_group": "dock-approach"},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="recovery-decided",
            event_type=EventType.TASK_DECIDED,
            timestamp="2026-06-14T13:00:15Z",
            summary="Retry with lower speed and wider approach corridor.",
            payload={"retry_group": "dock-approach"},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="recovery-acted",
            event_type=EventType.TASK_ACTED,
            timestamp="2026-06-14T13:00:25Z",
            summary="Robot executed recovery approach.",
            payload={"retry_group": "dock-approach"},
        ),
        create_memory_event(
            trace_id=trace_id,
            event_id="recovery-succeeded",
            event_type=EventType.TASK_SUCCEEDED,
            timestamp="2026-06-14T13:00:40Z",
            summary="Docking succeeded after recovery.",
        ),
    )
    trace = create_task_trace(
        trace_id=trace_id,
        task_name="dock-with-recovery",
        started_at="2026-06-14T13:00:00Z",
        events=events,
        ended_at="2026-06-14T13:00:40Z",
    )
    summary = summarize_experience(trace)
    return {
        "trace": model_to_dict(trace),
        "experience_summary": model_to_dict(summary),
    }


def main() -> None:
    print(json.dumps(build_trace_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
