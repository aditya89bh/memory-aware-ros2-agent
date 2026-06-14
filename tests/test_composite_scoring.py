import pytest

from memory_aware_ros2_agent.recall_engine import composite_scores


def test_composite_scores_combines_weighted_vectors() -> None:
    result = composite_scores(
        score_vectors=((1.0, 0.0), (0.5, 1.0)),
        weights=(2.0, 1.0),
    )

    assert result == pytest.approx((0.8333333333, 0.3333333333))


def test_composite_scores_returns_empty_for_no_vectors() -> None:
    assert composite_scores((), ()) == ()


def test_composite_scores_requires_matching_weight_count() -> None:
    with pytest.raises(ValueError, match="same length"):
        composite_scores(((1.0,),), ())


def test_composite_scores_requires_matching_vector_lengths() -> None:
    with pytest.raises(ValueError, match="same length"):
        composite_scores(((1.0,), (1.0, 0.5)), (1.0, 1.0))


def test_composite_scores_requires_positive_weight_sum() -> None:
    with pytest.raises(ValueError, match="positive"):
        composite_scores(((1.0,),), (0.0,))
