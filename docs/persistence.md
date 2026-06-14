# Persistence Layer

Phase 4 adds runtime-independent storage for memory events, task traces, and
recall results.

## Backends

- `InMemoryStore` keeps data in local dictionaries for tests and short-lived
  runs.
- `JsonFileStore` stores events, traces, and recall results in one JSON file.
- `SQLiteStore` stores records in SQLite tables with lookup indexes and schema
  metadata.
- `EventLogStore` appends memory events and recall results to a JSONL log and
  replays it on startup.

## Configuration

Use `PersistenceConfig` and `create_store_from_config()` to construct stores:

```python
from memory_aware_ros2_agent.persistence_config import (
    PersistenceConfig,
    create_store_from_config,
)

store = create_store_from_config(
    PersistenceConfig(backend="sqlite", path="memory.db")
)
```

Supported backend names are `memory`, `json`, `sqlite`, and `event_log`.

## APIs

The high-level API in `persistence_api.py` provides helpers for:

- Persisting and loading memory events.
- Persisting and loading task traces.
- Persisting and loading recall results.

Query helpers in `storage_queries.py` support common filters such as event type,
latest events, task name, and recall result timestamps.

## Maintenance

The persistence layer includes:

- Retention policies and pruning utilities.
- JSON, event-log, and SQLite corruption checks.
- File backup and restore helpers.
- SQLite migration helpers based on `schema_metadata`.

These utilities are intentionally local and deterministic so they can be used in
robot deployments without adding external services.
