"""Compatibility imports for ROS2 runtime dependencies."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any


class _FallbackLogger:
    def info(self, *_: Any, **__: Any) -> None:
        return None

    def warning(self, *_: Any, **__: Any) -> None:
        return None

    def error(self, *_: Any, **__: Any) -> None:
        return None


if TYPE_CHECKING:
    rclpy: Any

    class Node:
        """Typed fallback node used by static analysis."""

        def __init__(self, name: str, **kwargs: Any) -> None: ...
        def create_publisher(self, *args: Any, **kwargs: Any) -> Any: ...
        def create_subscription(self, *args: Any, **kwargs: Any) -> Any: ...
        def create_service(self, *args: Any, **kwargs: Any) -> Any: ...
        def get_logger(self) -> _FallbackLogger: ...
        def destroy_node(self) -> None: ...

    class String:
        """Typed fallback std_msgs/String message."""

        data: str

        def __init__(self, data: str = "") -> None: ...

    class Trigger:
        """Typed fallback std_srvs/Trigger service."""

        class Request:
            pass

        class Response:
            success: bool
            message: str

            def __init__(self) -> None: ...

else:
    try:
        import rclpy
        from rclpy.node import Node
        from std_msgs.msg import String
        from std_srvs.srv import Trigger
    except ImportError:  # pragma: no cover - used when ROS2 is not installed.
        rclpy = None

        class Node:
            """Fallback node used for local tests without ROS2 installed."""

            def __init__(self, name: str, **_: Any) -> None:
                self.name = name

            def create_publisher(self, *_: Any, **__: Any) -> Any:
                return None

            def create_subscription(self, *_: Any, **__: Any) -> Any:
                return None

            def create_service(self, *_: Any, **__: Any) -> Any:
                return None

            def get_logger(self) -> _FallbackLogger:
                return _FallbackLogger()

            def destroy_node(self) -> None:
                return None

        class String:
            """Fallback std_msgs/String message."""

            def __init__(self, data: str = "") -> None:
                self.data = data

        class Trigger:
            """Fallback std_srvs/Trigger service."""

            class Request:
                pass

            class Response:
                def __init__(self) -> None:
                    self.success = False
                    self.message = ""


__all__ = ["Node", "String", "Trigger", "rclpy", "ros_available"]


def ros_available() -> bool:
    """Return whether ROS2 Python modules are importable."""

    return rclpy is not None
