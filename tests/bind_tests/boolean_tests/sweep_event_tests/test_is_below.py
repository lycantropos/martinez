import pytest
from _martinez import (Point,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.leaf_sweep_events, strategies.points)
def test_leaf(event: SweepEvent, point: Point) -> None:
    with pytest.raises(ValueError):
        event.is_below(point)


@given(strategies.nested_sweep_events, strategies.points)
def test_nested(event: SweepEvent, point: Point) -> None:
    result = event.is_below(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(event: SweepEvent) -> None:
    assert not event.is_below(event.point)
