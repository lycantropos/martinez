import pytest
from _martinez import (Point,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.leaf_sweep_events, strategies.points)
def test_leaf(sweep_event: SweepEvent, point: Point) -> None:
    with pytest.raises(ValueError):
        sweep_event.is_below(point)


@given(strategies.nested_sweep_events, strategies.points)
def test_nested(sweep_event: SweepEvent, point: Point) -> None:
    result = sweep_event.is_below(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(sweep_event: SweepEvent) -> None:
    assert not sweep_event.is_below(sweep_event.point)
