"""Task replay demonstration."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import build_replay_steps


def build_demo_trace() -> TaskTrace:
    trace_id = "trace-replay-demo"
    return TaskTrace(
        trace_id=trace_id,
        task_name="replay-demo",
        started_at="2026-06-14T14:00:00Z",
        events=(
            MemoryEvent(
                "replay-started",
                trace_id,
                EventType.TASK_STARTED,
                "2026-06-14T14:00:00Z",
                "Task started.",
            ),
            MemoryEvent(
                "replay-acted",
                trace_id,
                EventType.TASK_ACTED,
                "2026-06-14T14:00:05Z",
                "Robot executed action.",
            ),
            MemoryEvent(
                "replay-succeeded",
                trace_id,
                EventType.TASK_SUCCEEDED,
                "2026-06-14T14:00:08Z",
                "Task succeeded.",
            ),
        ),
        ended_at="2026-06-14T14:00:08Z",
    )


def main() -> None:
    for step in build_replay_steps(build_demo_trace()):
        print(
            f"+{step.delay_since_previous_seconds:.1f}s "
            f"{step.event_type.value}: {step.summary}"
        )


if __name__ == "__main__":
    main()
