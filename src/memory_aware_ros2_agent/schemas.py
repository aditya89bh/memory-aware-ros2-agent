"""JSON schema helpers for memory models."""

from __future__ import annotations

from copy import deepcopy
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

JsonSchema = dict[str, Any]


def _object_schema(
    *,
    properties: dict[str, JsonSchema],
    required: list[str],
) -> JsonSchema:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required,
    }


_EVENT_SCHEMA = _object_schema(
    properties={
        "event_id": {"type": "string"},
        "trace_id": {"type": "string"},
        "event_type": {"type": "string", "enum": [event.value for event in EventType]},
        "timestamp": {"type": "string"},
        "summary": {"type": "string"},
        "payload": {"type": "object"},
    },
    required=["event_id", "trace_id", "event_type", "timestamp", "summary", "payload"],
)

_MODEL_SCHEMAS: dict[type[Any], JsonSchema] = {
    MemoryEvent: _EVENT_SCHEMA,
    TaskTrace: _object_schema(
        properties={
            "trace_id": {"type": "string"},
            "task_name": {"type": "string"},
            "started_at": {"type": "string"},
            "events": {"type": "array", "items": _EVENT_SCHEMA},
            "ended_at": {"type": ["string", "null"]},
        },
        required=["trace_id", "task_name", "started_at", "events", "ended_at"],
    ),
    RecallQuery: _object_schema(
        properties={
            "query_id": {"type": "string"},
            "query_text": {"type": "string"},
            "requested_at": {"type": "string"},
            "trace_id": {"type": ["string", "null"]},
            "limit": {"type": "integer"},
            "filters": {"type": "object"},
        },
        required=[
            "query_id",
            "query_text",
            "requested_at",
            "trace_id",
            "limit",
            "filters",
        ],
    ),
    RecallResult: _object_schema(
        properties={
            "query_id": {"type": "string"},
            "events": {"type": "array", "items": _EVENT_SCHEMA},
            "scores": {"type": "array", "items": {"type": "number"}},
            "generated_at": {"type": ["string", "null"]},
        },
        required=["query_id", "events", "scores", "generated_at"],
    ),
    EventMetadata: _object_schema(
        properties={
            "source_node_id": {"type": "string"},
            "created_at": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "priority": {"type": "integer"},
        },
        required=["source_node_id", "created_at", "tags", "priority"],
    ),
    TaskOutcome: _object_schema(
        properties={
            "trace_id": {"type": "string"},
            "status": {"type": "string"},
            "completed_at": {"type": "string"},
            "reason": {"type": ["string", "null"]},
            "metrics": {"type": "object"},
        },
        required=["trace_id", "status", "completed_at", "reason", "metrics"],
    ),
    SourceNode: _object_schema(
        properties={
            "node_id": {"type": "string"},
            "node_name": {"type": "string"},
            "namespace": {"type": "string"},
            "capabilities": {"type": "array", "items": {"type": "string"}},
        },
        required=["node_id", "node_name", "namespace", "capabilities"],
    ),
}


def schema_for_model(model_type: type[Any]) -> JsonSchema:
    """Return a JSON schema for a supported model type."""

    try:
        return deepcopy(_MODEL_SCHEMAS[model_type])
    except KeyError as exc:
        msg = f"No JSON schema registered for {model_type!r}"
        raise ValueError(msg) from exc


def schemas_for_all_models() -> dict[str, JsonSchema]:
    """Return JSON schemas keyed by model class name."""

    return {
        model_type.__name__: schema_for_model(model_type)
        for model_type in _MODEL_SCHEMAS
    }
