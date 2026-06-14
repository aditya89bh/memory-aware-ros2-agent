# Recall Engine

Phase 5 adds retrieval helpers for finding relevant memories from persisted
events, traces, and recall records.

## Engines

- `ExactMatchRecallEngine` matches query text against event summaries and
  payload text.
- `TaskBasedRecallEngine` retrieves events from traces whose task name matches
  the query.
- `TimeWindowRecallEngine` retrieves events inside a timestamp window.

## Filters

Recall queries can use `filters` to constrain retrieval:

- `event_types`: one or more event type values such as `task.failed`.
- `started_at` and `ended_at`: inclusive timestamp bounds.
- `metadata`: exact event payload key/value matches.
- `source_node_ids`: one or more source node identifiers from event payloads.
- `offset` and `page_size`: pagination controls.

## Scoring And Ranking

The recall engine utilities include:

- Recency scoring from event timestamps.
- Frequency scoring from repeated trace occurrences.
- Composite scoring with configurable weights.
- Stable score-based ranking and top-k retrieval.

## Example

```python
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import RecallQuery
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine

store = InMemoryStore()
query = RecallQuery(
    query_id="query-001",
    query_text="blocked dock",
    requested_at="2026-06-14T12:00:00Z",
    filters={"event_types": ("task.failed",)},
)

result = ExactMatchRecallEngine().recall(query, store)
```

## Evaluation

`recall_benchmarks.py` provides a small deterministic benchmark dataset.
`recall_metrics.py`, `recall_reports.py`, and `recall_visualizations.py` provide
precision/recall/F1 metrics, aggregate reports, and text visualizations.
