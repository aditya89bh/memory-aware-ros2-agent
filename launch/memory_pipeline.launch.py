"""Launch the core memory-aware ROS2 pipeline nodes."""

from __future__ import annotations

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Create a launch description for the core memory pipeline."""

    common_parameters = {
        "memory_events_topic": "memory/events",
        "memory_traces_topic": "memory/traces",
        "recall_service_name": "memory/recall",
        "queue_depth": 10,
    }
    return LaunchDescription(
        [
            Node(
                package="memory_aware_ros2_agent",
                executable="memory-recorder",
                name="memory_recorder",
                parameters=[common_parameters],
            ),
            Node(
                package="memory_aware_ros2_agent",
                executable="recall-service",
                name="recall_service",
                parameters=[common_parameters],
            ),
            Node(
                package="memory_aware_ros2_agent",
                executable="trace-publisher",
                name="trace_publisher",
                parameters=[common_parameters],
            ),
            Node(
                package="memory_aware_ros2_agent",
                executable="trace-subscriber",
                name="trace_subscriber",
                parameters=[common_parameters],
            ),
        ]
    )
