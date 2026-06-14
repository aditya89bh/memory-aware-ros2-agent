# Memory-Aware ROS2 Agent

Production-grade ROS2 package foundation for memory events, task traces, and recall in robot workflows.

This project provides a clean Python package that helps robot nodes record task
events, persist task traces, and recall relevant past events for future
decisions.

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

## Features Roadmap

- Memory event models for robot task workflows
- Task trace persistence for ordered execution history
- Recall interfaces for retrieving relevant prior events
- ROS2 node integration for publishing and consuming memory events
- Storage backends suitable for local development and robot deployment

## Installation

```sh
python -m pip install memory-aware-ros2-agent
```

For local development, install from a checkout with `python -m pip install -e
".[dev]"`.

## Development Setup

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Testing

```sh
pytest
ruff check .
mypy src
```

## ROS2 Usage

See [ROS2 Usage](docs/ros2_usage.md) for nodes, launch files, parameters, QoS,
lifecycle diagnostics, and validation commands.

See [Phase 3 Summary](docs/phase3_summary.md) for the completed ROS2
integration scope and deferred work.

See [Persistence Layer](docs/persistence.md) for Phase 4 storage backends,
configuration, retention, backup, restore, and migration utilities.

See [Phase 4 Summary](docs/phase4_summary.md) for the completed persistence
scope and deferred work.

See [Recall Engine](docs/recall_engine.md) for Phase 5 retrieval engines,
filters, scoring, ranking, evaluation metrics, and examples.

See [Phase 5 Summary](docs/phase5_summary.md) for the completed recall engine
scope and deferred work.

See [Trace Intelligence](docs/trace_intelligence.md) for Phase 6 analyzers,
benchmarks, reports, visualizations, and examples.

See [Phase 6 Summary](docs/phase6_summary.md) for the completed trace
intelligence scope and deferred work.

See [Production Readiness Checklist](docs/production_readiness_checklist.md)
and [Operations Guide](docs/operations.md) for Phase 7 hardening practices.

See [Phase 7 Summary](docs/phase7_summary.md) for the completed production
hardening scope and deferred work.

See [Developer Quickstart](docs/developer_quickstart.md),
[API Reference](docs/api_reference.md), [FAQ](docs/faq.md), and
[v1.0.0 Release Notes](docs/release_notes_v1.0.0.md) for the release-candidate
developer experience.

See [Phase 8 Summary](docs/phase8_summary.md) for final developer experience
and release validation results.

## Status

Phase 3 ROS2 integration, Phase 4 persistence, Phase 5 recall engine, Phase 6
trace intelligence, Phase 7 production hardening, and Phase 8 developer
experience/release preparation are complete for v1.0.0.
