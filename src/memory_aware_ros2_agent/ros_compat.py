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
        def declare_parameter(self, name: str, value: Any) -> Any: ...
        def create_publisher(self, *args: Any, **kwargs: Any) -> Any: ...
        def create_subscription(self, *args: Any, **kwargs: Any) -> Any: ...
        def create_service(self, *args: Any, **kwargs: Any) -> Any: ...
        def get_logger(self) -> _FallbackLogger: ...
        def destroy_node(self) -> None: ...

    class LifecycleNode(Node):
        """Typed fallback lifecycle node used by static analysis."""

    class SingleThreadedExecutor:
        """Typed fallback single-threaded executor."""

        def __init__(self, *args: Any, **kwargs: Any) -> None: ...
        def add_node(self, node: Node) -> bool: ...
        def spin(self) -> None: ...
        def shutdown(self) -> None: ...

    class MultiThreadedExecutor(SingleThreadedExecutor):
        """Typed fallback multi-threaded executor."""

    class QoSProfile:
        """Typed fallback QoS profile."""

        def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    class ReliabilityPolicy:
        """Typed fallback reliability policy enum."""

        RELIABLE: Any
        BEST_EFFORT: Any

    class DurabilityPolicy:
        """Typed fallback durability policy enum."""

        VOLATILE: Any
        TRANSIENT_LOCAL: Any

    class HistoryPolicy:
        """Typed fallback history policy enum."""

        KEEP_LAST: Any
        KEEP_ALL: Any

    class MutuallyExclusiveCallbackGroup:
        """Typed fallback mutually exclusive callback group."""

    class ReentrantCallbackGroup:
        """Typed fallback reentrant callback group."""

    class TransitionCallbackReturn:
        """Typed fallback transition return enum."""

        SUCCESS: Any
        FAILURE: Any

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
        from rclpy.callback_groups import (
            MutuallyExclusiveCallbackGroup,
            ReentrantCallbackGroup,
        )
        from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
        from rclpy.node import Node
        from rclpy.qos import (
            DurabilityPolicy,
            HistoryPolicy,
            QoSProfile,
            ReliabilityPolicy,
        )
        from std_msgs.msg import String
        from std_srvs.srv import Trigger

        try:
            from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn
        except ImportError:  # pragma: no cover - depends on ROS2 distribution.
            LifecycleNode = Node

            class TransitionCallbackReturn:
                SUCCESS = "success"
                FAILURE = "failure"
    except ImportError:  # pragma: no cover - used when ROS2 is not installed.
        rclpy = None

        class Node:
            """Fallback node used for local tests without ROS2 installed."""

            def __init__(self, name: str, **_: Any) -> None:
                self.name = name
                self._parameters: dict[str, Any] = {}

            def declare_parameter(self, name: str, value: Any) -> Any:
                self._parameters[name] = value
                return type("FallbackParameter", (), {"value": value})()

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

        class LifecycleNode(Node):
            """Fallback lifecycle node used without ROS2 installed."""

        class SingleThreadedExecutor:
            """Fallback executor used without ROS2 installed."""

            def __init__(self, **kwargs: Any) -> None:
                self.kwargs = kwargs
                self.nodes: list[Node] = []
                self.was_shutdown = False

            def add_node(self, node: Node) -> bool:
                self.nodes.append(node)
                return True

            def spin(self) -> None:
                return None

            def shutdown(self) -> None:
                self.was_shutdown = True

        class MultiThreadedExecutor(SingleThreadedExecutor):
            """Fallback multi-threaded executor used without ROS2 installed."""

        class ReliabilityPolicy:
            RELIABLE = "reliable"
            BEST_EFFORT = "best_effort"

        class DurabilityPolicy:
            VOLATILE = "volatile"
            TRANSIENT_LOCAL = "transient_local"

        class HistoryPolicy:
            KEEP_LAST = "keep_last"
            KEEP_ALL = "keep_all"

        class QoSProfile:
            """Fallback QoS profile used without ROS2 installed."""

            def __init__(
                self,
                *,
                depth: int,
                reliability: Any,
                durability: Any,
                history: Any,
            ) -> None:
                self.depth = depth
                self.reliability = reliability
                self.durability = durability
                self.history = history

        class MutuallyExclusiveCallbackGroup:
            """Fallback mutually exclusive callback group."""

        class ReentrantCallbackGroup:
            """Fallback reentrant callback group."""

        class TransitionCallbackReturn:
            SUCCESS = "success"
            FAILURE = "failure"

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


__all__ = [
    "DurabilityPolicy",
    "HistoryPolicy",
    "LifecycleNode",
    "MultiThreadedExecutor",
    "MutuallyExclusiveCallbackGroup",
    "Node",
    "QoSProfile",
    "ReliabilityPolicy",
    "ReentrantCallbackGroup",
    "SingleThreadedExecutor",
    "String",
    "TransitionCallbackReturn",
    "Trigger",
    "rclpy",
    "ros_available",
]


def ros_available() -> bool:
    """Return whether ROS2 Python modules are importable."""

    return rclpy is not None
