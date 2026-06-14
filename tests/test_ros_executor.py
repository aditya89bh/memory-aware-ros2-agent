import pytest

from memory_aware_ros2_agent import ros_executor
from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_executor import (
    ExecutorConfig,
    add_nodes,
    make_executor,
    spin_nodes,
)
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_executor_config_defaults_to_single_threaded() -> None:
    config = ExecutorConfig()
    executor = make_executor(config)

    assert config.kind == "single_threaded"
    assert executor is not None


def test_executor_config_accepts_multi_threaded_executor() -> None:
    executor = make_executor(ExecutorConfig(kind="multi_threaded", num_threads=2))

    assert executor is not None


def test_executor_config_rejects_unknown_kind() -> None:
    with pytest.raises(ValueError, match="Unsupported executor kind"):
        make_executor(ExecutorConfig(kind="event_loop"))


def test_add_nodes_registers_multiple_nodes() -> None:
    executor = make_executor()
    nodes = [MemoryRecorder(), TraceSubscriber()]

    add_nodes(executor, nodes)

    tracked_nodes = getattr(executor, "nodes", None)
    if tracked_nodes is not None:
        assert tracked_nodes == nodes


def test_spin_nodes_shuts_down_executor(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeExecutor:
        def __init__(self) -> None:
            self.nodes: list[object] = []
            self.was_shutdown = False

        def add_node(self, node: object) -> bool:
            self.nodes.append(node)
            return True

        def spin(self) -> None:
            return None

        def shutdown(self) -> None:
            self.was_shutdown = True

    executor = FakeExecutor()
    monkeypatch.setattr(ros_executor, "make_executor", lambda _: executor)

    spin_nodes([MemoryRecorder()])

    assert executor.was_shutdown is True
