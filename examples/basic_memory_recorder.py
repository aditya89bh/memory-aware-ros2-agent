"""Basic MemoryRecorder-style example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.factories import create_memory_event
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.serialization import model_to_dict


def main() -> None:
    event = create_memory_event(
        trace_id="trace-basic-recorder",
        event_type=EventType.TASK_OBSERVED,
        summary="Robot observed a ready workstation.",
        event_id="event-basic-observed",
        timestamp="2026-06-14T10:00:00Z",
        payload={"station": "workcell-a", "operator_present": False},
    )
    print(json.dumps(model_to_dict(event), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
