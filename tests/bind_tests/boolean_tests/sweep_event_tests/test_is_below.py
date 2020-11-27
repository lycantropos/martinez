import pytest
from hypothesis import given

from tests.bind_tests.hints import (BoundPoint, BoundSweepEvent)
from . import strategies


@given(strategies.leaf_sweep_events, strategies.points)
def test_leaf(event: BoundSweepEvent, point: BoundPoint) -> None:
    with pytest.raises(ValueError):
        event.is_below(point)


@given(strategies.nested_sweep_events, strategies.points)
def test_nested(event: BoundSweepEvent, point: BoundPoint) -> None:
    result = event.is_below(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(event: BoundSweepEvent) -> None:
    assert not event.is_below(event.point)
