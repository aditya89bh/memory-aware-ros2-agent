# Trace Intelligence

Phase 6 turns raw task traces into operational insight. The trace intelligence
helpers analyze ordered `TaskTrace` events and return deterministic summaries,
patterns, anomalies, and replay data that can be used by ROS2 nodes, reports,
or future decision support.

## Analyzer Interface

Use `TraceAnalyzer` for components that turn one `TaskTrace` into a
`TraceInsight`. Concrete analyzers include duration, failure patterns, success
patterns, event sequence extraction, repeated failure detection, anomaly
detection, retry chains, state transitions, bottlenecks, outcome summaries,
execution statistics, and experience summaries.

## Core Helpers

- `task_duration_seconds(trace)` calculates trace duration from `ended_at` or
  the latest event timestamp.
- `failure_pattern_counts(trace)` and `success_pattern_counts(trace)` summarize
  repeated operational signals.
- `extract_event_sequence(trace)` produces timestamp-ordered event steps.
- `detect_repeated_failures(trace)` finds failure reasons that occur multiple
  times.
- `detect_trace_anomalies(trace)` flags missing terminal outcomes, excessive
  duration, and failures after success.
- `analyze_retry_chains(trace)` groups retry attempts by `retry_group` payload.
- `analyze_state_transitions(trace)` counts adjacent event-type transitions.
- `identify_bottlenecks(trace, minimum_gap_seconds=...)` finds long event gaps.
- `summarize_outcome(trace)` and `summarize_experience(trace)` produce compact
  operational summaries.

## Benchmarking And Reports

`default_trace_analyzer_benchmark_dataset()` provides deterministic traces for
success, repeated failure, and anomaly scenarios.
`build_trace_analyzer_benchmark_report(dataset)` scores analyzer outputs against
expected traits. Text renderers in `trace_intelligence_visualizations.py`
produce stable report and experience summary output for CLI tools and demos.

## Example

```python
from memory_aware_ros2_agent.trace_intelligence import (
    ExperienceSummaryAnalyzer,
)

insight = ExperienceSummaryAnalyzer().analyze(trace)
print(insight.summary)
```

## Validation

Trace intelligence is covered by focused unit tests and benchmark tests. Run:

```sh
pytest tests/test_*trace* tests/test_*anomaly* tests/test_*replay*
ruff check .
mypy src
```
