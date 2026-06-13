# Architecture

`memory-aware-ros2-agent` is intended to provide a small memory layer for robot
workflows. The package will let robot nodes record what happened during a task,
persist those events as task traces, and recall relevant prior context before
future decisions.

## Phase 1 Scope

This phase only establishes the repository foundation:

- Python package structure
- Tooling for linting, typing, and tests
- Initial documentation
- Minimal import test

No ROS2 runtime code is included yet.

## Initial Components

```text
Robot Node
  emits task event data

Memory Event API
  validates and records task events

Task Trace Store
  persists ordered events from a workflow

Recall Interface
  retrieves relevant past events for decision support
```

## Design Direction

The package should stay small and composable. ROS2 nodes, message definitions,
storage backends, and recall strategies should be added only when their
interfaces are clear from concrete workflow examples.
