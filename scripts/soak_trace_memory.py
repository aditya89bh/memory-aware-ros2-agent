"""Long-running soak harness for memory persistence and recall."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.factories import create_memory_event, create_recall_query
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine


def run_soak(iterations: int, sleep_seconds: float) -> int:
    """Run repeated store writes and recall reads."""

    store = InMemoryStore()
    engine = ExactMatchRecallEngine()
    for index in range(iterations):
        store.save_event(
            create_memory_event(
                trace_id="trace-soak",
                event_type=EventType.TASK_OBSERVED,
                summary=f"Soak observation {index}",
                event_id=f"event-{index}",
            )
        )
        query = create_recall_query(
            query_text="soak",
            query_id=f"query-{index}",
            trace_id="trace-soak",
            limit=iterations,
        )
        result = engine.recall(query, store)
        if not result.events:
            raise RuntimeError("soak recall returned no events")
        if sleep_seconds:
            time.sleep(sleep_seconds)
    return len(store.list_events("trace-soak"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    args = parser.parse_args()
    event_count = run_soak(args.iterations, args.sleep_seconds)
    print(f"soak completed: {event_count} events")


if __name__ == "__main__":
    main()
