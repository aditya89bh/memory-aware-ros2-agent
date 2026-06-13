"""ROS2 setup entry point for ament_python."""

from setuptools import find_packages, setup

PACKAGE_NAME = "memory_aware_ros2_agent"

setup(
    name=PACKAGE_NAME,
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{PACKAGE_NAME}"]),
        (f"share/{PACKAGE_NAME}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Aditya Bhatia",
    maintainer_email="aditya89bh@gmail.com",
    description="ROS2 package for memory events, task traces, and recall in robot workflows.",
    license="MIT",
    entry_points={
        "console_scripts": [],
    },
)
