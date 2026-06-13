from datetime import datetime, timezone

from memory_aware_ros2_agent.time_utils import format_utc_timestamp, utc_now_iso


def test_format_utc_timestamp_uses_z_suffix() -> None:
    timestamp = datetime(2026, 6, 13, 5, 0, 0, tzinfo=timezone.utc)

    assert format_utc_timestamp(timestamp) == "2026-06-13T05:00:00Z"


def test_format_utc_timestamp_treats_naive_datetime_as_utc() -> None:
    timestamp = datetime(2026, 6, 13, 5, 0, 0)

    assert format_utc_timestamp(timestamp) == "2026-06-13T05:00:00Z"


def test_utc_now_iso_returns_utc_string() -> None:
    assert utc_now_iso().endswith("Z")
