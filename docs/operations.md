# Operations Guide

This guide covers operational checks for running `memory-aware-ros2-agent` in a
ROS2-oriented environment.

## Deployment Checks

1. Install the package from a validated wheel or source checkout.
2. Run `memory-recorder`, `trace-publisher`, and `trace-subscriber` in a test
   namespace before using production topics.
3. Confirm configured persistence backend paths are writable by the runtime
   user.
4. Run `colcon build` in the target workspace.

## Runtime Validation

- Use `pytest`, `ruff check .`, and `mypy src` before publishing changes.
- Run `scripts/soak_trace_memory.py --iterations 1000` for pre-release soak
  validation.
- Use the load fixtures and benchmark helpers to compare performance-sensitive
  changes.

## Observability

- Monitor ROS2 node logs for startup validation failures.
- Track trace counts, event counts, recall result counts, and persistence
  backend errors.
- Preserve generated SBOMs and release artifact hashes for audit trails.

## Recovery

- For JSON and SQLite backends, restore from the latest validated backup.
- For append-only event logs, replay the log and inspect corruption reports
  before pruning.
- If recall or trace intelligence behavior regresses, rerun benchmark datasets
  and compare against committed snapshots.
