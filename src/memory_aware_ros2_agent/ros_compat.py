"""Compatibility imports for ROS2 runtime dependencies."""

from __future__ import annotations

from typing import Any

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
    from std_srvs.srv import Trigger
except ImportError:  # pragma: no cover - exercised when ROS2 is not installed.
    rclpy = None  # type: ignore[assignment]

    class Node:  # type: ignore[no-redef]
        """Fallback node used for local tests without ROS2 installed."""

        def __init__(self, name: str, **_: Any) -> None:
            self.name = name

        def create_publisher(self, *_: Any, **__: Any) -> Any:
            return None

        def create_subscription(self, *_: Any, **__: Any) -> Any:
            return None

        def create_service(self, *_: Any, **__: Any) -> Any:
            return None

        def get_logger(self) -> Any:
            return _FallbackLogger()

    class String:  # type: ignore[no-redef]
        """Fallback std_msgs/String message."""

        def __init__(self, data: str = "") -> None:
            self.data = data

    class Trigger:  # type: ignore[no-redef]
        """Fallback std_srvs/Trigger service."""

        class Request:
            pass

        class Response:
            def __init__(self) -> None:
                self.success = False
                self.message = ""


class _FallbackLogger:
    def info(self, *_: Any, **__: Any) -> None:
        return None

    def warning(self, *_: Any, **__: Any) -> None:
        return None

    def error(self, *_: Any, **__: Any) -> None:
        return None


def ros_available() -> bool:
    """Return whether ROS2 Python modules are importable."""

    return rclpy is not None
