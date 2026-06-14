"""ROS2 setup entry point for ament_python."""

from glob import glob

from setuptools import find_packages, setup

PACKAGE_NAME = "memory_aware_ros2_agent"

setup(
    name=PACKAGE_NAME,
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{PACKAGE_NAME}"]),
        (f"share/{PACKAGE_NAME}", ["package.xml"]),
        (f"share/{PACKAGE_NAME}/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Aditya Bhatia",
    maintainer_email="aditya89bh@gmail.com",
    description=(
        "ROS2 package for memory events, task traces, and recall in robot workflows."
    ),
    license="MIT",
    entry_points={
        "console_scripts": [
            "memory-benchmark = memory_aware_ros2_agent.cli:benchmark_main",
            "memory-export = memory_aware_ros2_agent.cli:export_main",
            "memory-import = memory_aware_ros2_agent.cli:import_main",
            "memory-inspect = memory_aware_ros2_agent.cli:inspect_main",
            "memory-lifecycle = memory_aware_ros2_agent.lifecycle_node:main",
            "memory-recorder = memory_aware_ros2_agent.memory_recorder_node:main",
            "recall-service = memory_aware_ros2_agent.recall_service_node:main",
            "trace-publisher = memory_aware_ros2_agent.trace_publisher_node:main",
            "trace-subscriber = memory_aware_ros2_agent.trace_subscriber_node:main",
        ],
    },
)
