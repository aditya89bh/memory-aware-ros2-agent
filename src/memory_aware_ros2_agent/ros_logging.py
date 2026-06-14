"""Structured logging helpers for ROS2 nodes."""

from __future__ import annotations

import json
from typing import Any


def structured_log_message(event: str, **fields: Any) -> str:
    """Create a deterministic structured log message."""

    payload = {"event": event, **fields}
    return json.dumps(payload, sort_keys=True)


def log_info(logger: Any, event: str, **fields: Any) -> None:
    """Emit a structured info-level ROS log."""

    logger.info(structured_log_message(event, **fields))


def log_error(logger: Any, event: str, **fields: Any) -> None:
    """Emit a structured error-level ROS log."""

    logger.error(structured_log_message(event, **fields))
