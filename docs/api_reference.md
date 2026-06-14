# API Reference

## Core Models

- `memory_aware_ros2_agent.models` defines `MemoryEvent`, `TaskTrace`,
  `RecallQuery`, `RecallResult`, `SourceNode`, `EventMetadata`, and
  `TaskOutcome`.
- `memory_aware_ros2_agent.factories` provides helpers for creating events,
  traces, recall queries, and recall results with generated defaults.
- `memory_aware_ros2_agent.serialization` converts models to JSON-compatible
  dictionaries and back.

## Persistence

- `memory_aware_ros2_agent.memory_store` defines the `MemoryStore` protocol.
- `memory_aware_ros2_agent.in_memory_store`, `json_file_store`,
  `sqlite_store`, and `event_log_store` provide concrete backends.
- `memory_aware_ros2_agent.persistence_api` offers high-level event, trace, and
  recall record persistence helpers.

## Recall

- `memory_aware_ros2_agent.recall_engine` defines recall engine protocols and
  exact, task-based, and time-window recall engines.
- `memory_aware_ros2_agent.recall_scoring`,
  `memory_aware_ros2_agent.recall_filters`, and
  `memory_aware_ros2_agent.recall_ranking` provide composable retrieval
  building blocks.

## Trace Intelligence

- `memory_aware_ros2_agent.trace_intelligence` contains analyzers for duration,
  failures, successes, sequences, retries, anomalies, state transitions,
  bottlenecks, replay steps, and experience summaries.

## Developer CLIs

- `memory-inspect` summarizes a JSON event or trace.
- `memory-export` bundles JSON memory records.
- `memory-import` unpacks exported bundles.
- `memory-benchmark` runs deterministic performance benchmarks.
