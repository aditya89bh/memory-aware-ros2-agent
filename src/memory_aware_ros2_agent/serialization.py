"""Serialization helpers for memory models."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any

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
