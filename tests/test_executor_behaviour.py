import pytest

from memory_aware_ros2_agent import ros_executor
from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_executor import add_nodes, spin_nodes
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


class FakeExecutor:
    def __init__(self, fail_on_spin: bool = False) -> None:
        self.fail_on_spin = fail_on_spin
        self.nodes: list[object] = []
        self.was_shutdown = False

    def add_node(self, node: object) -> bool:
        self.nodes.append(node)
        return True

    def spin(self) -> None:
        if self.fail_on_spin:
            raise RuntimeError("spin failed")

    def shutdown(self) -> None:
        self.was_shutdown = True


def test_add_nodes_preserves_registration_order() -> None:
    executor = FakeExecutor()
    nodes = [MemoryRecorder(), TraceSubscriber()]

    add_nodes(executor, nodes)

    assert executor.nodes == nodes


def test_spin_nodes_shuts_down_when_spin_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executor = FakeExecutor()
    monkeypatch.setattr(ros_executor, "make_executor", lambda _: executor)

    spin_nodes([MemoryRecorder()])

    assert executor.was_shutdown is True


def test_spin_nodes_shuts_down_when_spin_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executor = FakeExecutor(fail_on_spin=True)
    monkeypatch.setattr(ros_executor, "make_executor", lambda _: executor)

    with pytest.raises(RuntimeError, match="spin failed"):
        spin_nodes([MemoryRecorder()])

    assert executor.was_shutdown is True
