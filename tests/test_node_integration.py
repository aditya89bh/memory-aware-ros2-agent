import json

from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.models import MemoryEvent, TaskTrace
from memory_aware_ros2_agent.ros_compat import String
from memory_aware_ros2_agent.serialization import model_to_dict
from memory_aware_ros2_agent.trace_publisher_node import TracePublisher
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_trace_publisher_message_can_be_recorded_by_trace_subscriber() -> None:
    publisher = TracePublisher()
    subscriber = TraceSubscriber()
    trace = TaskTrace(
        trace_id="trace-integration",
        task_name="inspect",
        started_at="2026-06-14T09:00:00Z",
    )

    subscriber.record_trace(publisher.serialize_trace(trace))

    assert subscriber.last_trace is not None
    assert subscriber.last_trace.trace_id == "trace-integration"
    assert subscriber.last_trace.task_name == "inspect"


def test_trace_subscriber_preserves_nested_memory_events() -> None:
    event = MemoryEvent(
        event_id="event-integration",
        trace_id="trace-integration",
        event_type="task.started",
        timestamp="2026-06-14T09:00:00Z",
        summary="Task started.",
    )
    trace = TaskTrace(
        trace_id="trace-integration",
        task_name="inspect",
        started_at="2026-06-14T09:00:00Z",
        events=(event,),
    )
    subscriber = TraceSubscriber()

    subscriber.record_trace(String(data=json.dumps(model_to_dict(trace))))

    assert subscriber.last_trace is not None
    assert subscriber.last_trace.events[0].event_id == "event-integration"


def test_memory_recorder_and_trace_subscriber_share_trace_ids() -> None:
    recorder = MemoryRecorder()
    subscriber = TraceSubscriber()

    recorder.record_event(
        String(
            data=json.dumps(
                {
                    "event_id": "event-integration",
                    "trace_id": "trace-integration",
                    "event_type": "task.started",
                    "timestamp": "2026-06-14T09:00:00Z",
                    "summary": "Task started.",
                    "payload": {},
                }
            )
        )
    )
    subscriber.record_trace(
        String(
            data=json.dumps(
                {
                    "trace_id": "trace-integration",
                    "task_name": "inspect",
                    "started_at": "2026-06-14T09:00:00Z",
                    "events": [],
                }
            )
        )
    )

    assert recorder.last_event is not None
    assert subscriber.last_trace is not None
    assert recorder.last_event.trace_id == subscriber.last_trace.trace_id
