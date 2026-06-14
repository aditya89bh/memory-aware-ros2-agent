"""Launch the memory lifecycle node."""

from __future__ import annotations

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Create a launch description for the memory lifecycle node."""

    return LaunchDescription(
        [
            Node(
                package="memory_aware_ros2_agent",
                executable="memory-lifecycle",
                name="memory_lifecycle",
                parameters=[
                    {
                        "memory_events_topic": "memory/events",
                        "memory_traces_topic": "memory/traces",
                        "recall_service_name": "memory/recall",
                        "queue_depth": 10,
                    }
                ],
            )
        ]
    )
