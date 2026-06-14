# v1.0.0 Release Notes

`memory-aware-ros2-agent` v1.0.0 is the first release candidate for a polished
open-source ROS2 memory layer for robot task experience.

## Highlights

- Core memory models for events, task traces, recall queries, and recall
  results.
- ROS2 nodes, launch examples, lifecycle support, QoS configuration, diagnostics,
  and structured logging.
- Persistence backends for in-memory, JSON file, SQLite, and append-only event
  log storage.
- Recall engines with filtering, scoring, ranking, query planning, and
  explanations.
- Trace intelligence analyzers for duration, failures, retries, anomalies,
  bottlenecks, replay, and summaries.
- Developer examples, sample datasets, CLIs, diagrams, and release docs.

## Validation Gates

The release candidate is expected to pass:

```bash
pytest
ruff check .
mypy src
python -m build
colcon build
```

## Known Limitations

- Demo GIF assets are placeholders until a full visual walkthrough is recorded.
- Recall examples use deterministic local data rather than large production
  traces.
