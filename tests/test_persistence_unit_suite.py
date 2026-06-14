from pathlib import Path

from memory_aware_ros2_agent.backup import create_backup
from memory_aware_ros2_agent.corruption import check_json_file
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.persistence_api import persist_event
from memory_aware_ros2_agent.persistence_config import (
    PersistenceConfig,
    create_store_from_config,
)
from memory_aware_ros2_agent.restore import restore_backup
from memory_aware_ros2_agent.retention import RetentionPolicy
from memory_aware_ros2_agent.storage_queries import events_by_type


def test_persistence_unit_flow_uses_public_helpers(tmp_path: Path) -> None:
    store = InMemoryStore()
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )

    persist_event(store, event)

    assert events_by_type(store, EventType.TASK_STARTED) == (event,)
    assert RetentionPolicy(max_events=1).max_events == 1


def test_persistence_file_unit_flow_checks_backup_restore_and_config(
    tmp_path: Path,
) -> None:
    active_path = tmp_path / "memory.json"
    active_path.write_text('{"events": {}, "traces": {}}', encoding="utf-8")
    backup = create_backup(active_path, tmp_path / "backups")
    active_path.unlink()

    restore_backup(backup.backup_path, active_path)

    assert check_json_file(active_path).is_corrupt is False
    assert create_store_from_config(
        PersistenceConfig(backend="json", path=str(active_path))
    )
