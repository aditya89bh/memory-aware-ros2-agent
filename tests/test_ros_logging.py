import json

from memory_aware_ros2_agent.ros_logging import (
    log_error,
    log_info,
    structured_log_message,
)


class RecordingLogger:
    def __init__(self) -> None:
        self.info_messages: list[str] = []
        self.error_messages: list[str] = []

    def info(self, message: str) -> None:
        self.info_messages.append(message)

    def error(self, message: str) -> None:
        self.error_messages.append(message)


def test_structured_log_message_includes_event_and_fields() -> None:
    message = structured_log_message("task_trace_recorded", trace_id="trace-001")

    payload = json.loads(message)
    assert payload == {"event": "task_trace_recorded", "trace_id": "trace-001"}


def test_log_info_emits_structured_message() -> None:
    logger = RecordingLogger()

    log_info(logger, "memory_event_recorded", event_id="event-001")

    assert json.loads(logger.info_messages[0])["event"] == "memory_event_recorded"


def test_log_error_emits_structured_message() -> None:
    logger = RecordingLogger()

    log_error(logger, "memory_event_record_failed", error="bad payload")

    assert json.loads(logger.error_messages[0])["error"] == "bad payload"
