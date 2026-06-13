"""Serialization helpers for memory models."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any

from memory_aware_ros2_agent.models import (
    EventMetadata,
    EventType,
    MemoryEvent,
    RecallQuery,
    RecallResult,
    SourceNode,
    TaskOutcome,
    TaskTrace,
)

JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]


def to_serializable(value: Any) -> JsonValue:
    """Convert model values into JSON-compatible Python values."""

    if isinstance(value, Enum):
        return value.value

    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: to_serializable(getattr(value, field.name))
            for field in fields(value)
        }

    if isinstance(value, (list, tuple)):
        return [to_serializable(item) for item in value]

    if isinstance(value, dict):
        return {str(key): to_serializable(item) for key, item in value.items()}

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    msg = f"Unsupported value for serialization: {type(value).__name__}"
    raise TypeError(msg)


def model_to_dict(model: object) -> dict[str, JsonValue]:
    """Serialize a model into a JSON-compatible dictionary."""

    serialized = to_serializable(model)
    if not isinstance(serialized, dict):
        msg = f"Expected model serialization to produce a dict, got {type(serialized).__name__}"
        raise TypeError(msg)
    return serialized


def memory_event_from_dict(data: dict[str, Any]) -> MemoryEvent:
    """Deserialize a memory event from a dictionary."""

    return MemoryEvent(
        event_id=str(data["event_id"]),
        trace_id=str(data["trace_id"]),
        event_type=EventType(str(data["event_type"])),
        timestamp=str(data["timestamp"]),
        summary=str(data["summary"]),
        payload=dict(data.get("payload", {})),
    )


def task_trace_from_dict(data: dict[str, Any]) -> TaskTrace:
    """Deserialize a task trace from a dictionary."""

    events = tuple(memory_event_from_dict(item) for item in data.get("events", ()))
    ended_at = data.get("ended_at")
    return TaskTrace(
        trace_id=str(data["trace_id"]),
        task_name=str(data["task_name"]),
        started_at=str(data["started_at"]),
        events=events,
        ended_at=None if ended_at is None else str(ended_at),
    )


def recall_query_from_dict(data: dict[str, Any]) -> RecallQuery:
    """Deserialize a recall query from a dictionary."""

    trace_id = data.get("trace_id")
    return RecallQuery(
        query_id=str(data["query_id"]),
        query_text=str(data["query_text"]),
        requested_at=str(data["requested_at"]),
        trace_id=None if trace_id is None else str(trace_id),
        limit=int(data.get("limit", 5)),
        filters=dict(data.get("filters", {})),
    )


def recall_result_from_dict(data: dict[str, Any]) -> RecallResult:
    """Deserialize a recall result from a dictionary."""

    generated_at = data.get("generated_at")
    return RecallResult(
        query_id=str(data["query_id"]),
        events=tuple(memory_event_from_dict(item) for item in data.get("events", ())),
        scores=tuple(float(score) for score in data.get("scores", ())),
        generated_at=None if generated_at is None else str(generated_at),
    )


def event_metadata_from_dict(data: dict[str, Any]) -> EventMetadata:
    """Deserialize event metadata from a dictionary."""

    return EventMetadata(
        source_node_id=str(data["source_node_id"]),
        created_at=str(data["created_at"]),
        tags=tuple(str(tag) for tag in data.get("tags", ())),
        priority=int(data.get("priority", 0)),
    )


def task_outcome_from_dict(data: dict[str, Any]) -> TaskOutcome:
    """Deserialize a task outcome from a dictionary."""

    reason = data.get("reason")
    return TaskOutcome(
        trace_id=str(data["trace_id"]),
        status=str(data["status"]),
        completed_at=str(data["completed_at"]),
        reason=None if reason is None else str(reason),
        metrics=dict(data.get("metrics", {})),
    )


def source_node_from_dict(data: dict[str, Any]) -> SourceNode:
    """Deserialize a source node from a dictionary."""

    return SourceNode(
        node_id=str(data["node_id"]),
        node_name=str(data["node_name"]),
        namespace=str(data.get("namespace", "/")),
        capabilities=tuple(str(capability) for capability in data.get("capabilities", ())),
    )
