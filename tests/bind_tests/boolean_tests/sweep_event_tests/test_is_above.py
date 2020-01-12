import pytest
from _martinez import (Point,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.leaf_sweep_events, strategies.points)
def test_leaf(event: SweepEvent, point: Point) -> None:
    with pytest.raises(ValueError):
        event.is_above(point)


@given(strategies.nested_sweep_events, strategies.points)
def test_nested(event: SweepEvent, point: Point) -> None:
    result = event.is_above(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(event: SweepEvent) -> None:
    assert event.is_above(event.point)


@given(strategies.nested_sweep_events, strategies.points)
def test_alternatives(event: SweepEvent, point: Point) -> None:
    assert event.is_above(point) or event.is_below(point)
