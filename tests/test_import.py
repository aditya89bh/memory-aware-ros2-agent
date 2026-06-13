def test_package_imports() -> None:
    import memory_aware_ros2_agent

    assert memory_aware_ros2_agent is not None


def test_package_name_export() -> None:
    from memory_aware_ros2_agent import PACKAGE_NAME

    assert PACKAGE_NAME == "memory-aware-ros2-agent"
