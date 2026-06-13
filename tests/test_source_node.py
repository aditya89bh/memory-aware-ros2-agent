from memory_aware_ros2_agent.models import SourceNode


def test_source_node_stores_node_identity() -> None:
    node = SourceNode(
        node_id="planner-node",
        node_name="task_planner",
        namespace="/robot_1",
        capabilities=("planning", "recovery"),
    )

    assert node.node_id == "planner-node"
    assert node.node_name == "task_planner"
    assert node.namespace == "/robot_1"
    assert node.capabilities == ("planning", "recovery")


def test_source_node_defaults_namespace_and_capabilities() -> None:
    node = SourceNode(node_id="memory-node", node_name="memory")

    assert node.namespace == "/"
    assert node.capabilities == ()
