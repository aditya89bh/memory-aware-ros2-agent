import os
from collections.abc import Generator
from pathlib import Path

import pytest

from memory_aware_ros2_agent.ros_compat import rclpy


@pytest.fixture(scope="session", autouse=True)
def ros_context() -> Generator[None, None, None]:
    if rclpy is None:
        yield
        return

    log_dir = Path(".ros-log")
    log_dir.mkdir(exist_ok=True)
    os.environ.setdefault("ROS_LOG_DIR", str(log_dir.resolve()))

    rclpy.init()
    try:
        yield
    finally:
        rclpy.shutdown()
