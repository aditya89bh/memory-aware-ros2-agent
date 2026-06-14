from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.persistence import MemoryStore


class StubMemoryStore:
    def __init__(self) -> None:
        self.events: dict[str, MemoryEvent] = {}
        self.traces: dict[str, TaskTrace] = {}

    def save_event(self, event: MemoryEvent) -> None:
        self.events[event.event_id] = event

    def get_event(self, event_id: str) -> MemoryEvent | None:
        return self.events.get(event_id)

    def list_events(self, trace_id: str | None = None) -> tuple[MemoryEvent, ...]:
        events = tuple(self.events.values())
        if trace_id is None:
            return events
        return tuple(event for event in events if event.trace_id == trace_id)

    def save_trace(self, trace: TaskTrace) -> None:
        self.traces[trace.trace_id] = trace

    def get_trace(self, trace_id: str) -> TaskTrace | None:
        return self.traces.get(trace_id)

    def list_traces(self) -> tuple[TaskTrace, ...]:
        return tuple(self.traces.values())

    def close(self) -> None:
        return None


def test_memory_store_protocol_supports_events_and_traces() -> None:
    store: MemoryStore = StubMemoryStore()
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="inspect",
        started_at="2026-06-14T10:00:00Z",
        events=(event,),
    )

    store.save_event(event)
    store.save_trace(trace)

    assert store.get_event("event-001") == event
    assert store.list_events("trace-001") == (event,)
    assert store.get_trace("trace-001") == trace
    assert store.list_traces() == (trace,)
