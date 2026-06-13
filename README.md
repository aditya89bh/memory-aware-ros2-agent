# Memory-Aware ROS2 Agent

ROS2 package foundation for memory events, task traces, and recall in robot workflows.

This project will provide a clean Python package that helps robot nodes record task events,
persist task traces, and recall relevant past events for future decisions. Phase 1 keeps the
repository intentionally minimal: package structure, tooling, docs, and tests only.

## Why Memory-Aware Robotics Matters

Robots often repeat similar workflows across changing environments. Without task memory, a
robot can lose useful context about prior attempts, failures, operator interventions, and
successful recovery paths. A memory-aware robot workflow can make future decisions with more
continuity by preserving what happened, when it happened, and why it mattered.

## Early Architecture

```text
Robot Node
  |
  | records task events
  v
Memory Event API
  |
  | groups events into traces
  v
Task Trace Store
  |
  | retrieves relevant prior context
  v
Recall Interface
  |
  | returns context for future decisions
  v
Robot Workflow
```

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Tests

```sh
pytest
ruff check .
mypy
```

## Status

Initial repository foundation only. ROS2 runtime nodes, messages, launch files, and storage
implementations will be added in later phases.
