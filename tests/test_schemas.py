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
from memory_aware_ros2_agent.schemas import schema_for_model, schemas_for_all_models


def test_schemas_are_registered_for_all_models() -> None:
    schemas = schemas_for_all_models()

    assert set(schemas) == {
        "EventMetadata",
        "MemoryEvent",
        "RecallQuery",
        "RecallResult",
        "SourceNode",
        "TaskOutcome",
        "TaskTrace",
    }


def test_memory_event_schema_contains_required_fields() -> None:
    schema = schema_for_model(MemoryEvent)

    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "event_id",
        "trace_id",
        "event_type",
        "timestamp",
        "summary",
        "payload",
    }


def test_memory_event_schema_lists_event_type_values() -> None:
    schema = schema_for_model(MemoryEvent)

    assert schema["properties"]["event_type"]["enum"] == [
        event.value for event in EventType
    ]


def test_schema_for_model_rejects_unknown_types() -> None:
    class UnknownModel:
        pass

    try:
        schema_for_model(UnknownModel)
    except ValueError as exc:
        assert "No JSON schema registered" in str(exc)
    else:
        raise AssertionError("Expected unsupported model type to raise ValueError")


def test_all_model_schemas_have_required_lists() -> None:
    for model_type in (
        EventMetadata,
        MemoryEvent,
        RecallQuery,
        RecallResult,
        SourceNode,
        TaskOutcome,
        TaskTrace,
    ):
        schema = schema_for_model(model_type)
        assert isinstance(schema["required"], list)
        assert schema["required"]
