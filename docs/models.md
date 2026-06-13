# Core Memory Models

Phase 2 defines the data structures that later ROS2 integration and storage
layers will use.

## MemoryEvent

`MemoryEvent` records one notable point in a robot task workflow.

```python
from memory_aware_ros2_agent import EventType, MemoryEvent

event = MemoryEvent(
    event_id="event-001",
    trace_id="trace-001",
    event_type=EventType.TASK_STARTED,
    timestamp="2026-06-13T05:00:00Z",
    summary="Robot started pick workflow.",
)
```

## TaskTrace

`TaskTrace` groups ordered events for one task execution.

```python
from memory_aware_ros2_agent import TaskTrace

trace = TaskTrace(
    trace_id="trace-001",
    task_name="pick-and-place",
    started_at="2026-06-13T05:00:00Z",
    events=(event,),
)
```

## RecallQuery And RecallResult

`RecallQuery` describes what prior context is needed. `RecallResult` carries the
matching events and optional relevance scores.

```python
from memory_aware_ros2_agent import RecallQuery, RecallResult

query = RecallQuery(
    query_id="query-001",
    query_text="What happened during the previous grasp failure?",
    requested_at="2026-06-13T05:10:00Z",
)

result = RecallResult(query_id=query.query_id, events=(event,), scores=(0.92,))
```

## Supporting Models

- `EventMetadata` stores source, tags, and priority context.
- `SourceNode` identifies the node that produced memory data.
- `TaskOutcome` summarizes task completion status and metrics.
- `EventType` defines stable event categories.
