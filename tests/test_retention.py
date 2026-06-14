import pytest

from memory_aware_ros2_agent.retention import RetentionPolicy, keep_newest_count


def test_retention_policy_defaults_to_unbounded() -> None:
    policy = RetentionPolicy()

    assert policy.max_events is None
    assert policy.max_traces is None
    assert policy.max_recall_results is None


def test_retention_policy_rejects_negative_limits() -> None:
    with pytest.raises(ValueError, match="max_events"):
        RetentionPolicy(max_events=-1)


def test_keep_newest_count_returns_oldest_record_count_to_prune() -> None:
    assert keep_newest_count(total_count=5, max_count=3) == 2
    assert keep_newest_count(total_count=2, max_count=3) == 0
    assert keep_newest_count(total_count=5, max_count=None) == 0
