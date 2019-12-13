import pytest
from hypothesis import given

from martinez.boolean import SweepEvent
from martinez.point import Point
from . import strategies


@given(strategies.leaf_sweep_events, strategies.points)
def test_leaf(sweep_event: SweepEvent, point: Point) -> None:
    with pytest.raises(ValueError):
        sweep_event.is_above(point)


@given(strategies.nested_sweep_events, strategies.points)
def test_nested(sweep_event: SweepEvent, point: Point) -> None:
    result = sweep_event.is_above(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(sweep_event: SweepEvent) -> None:
    assert sweep_event.is_above(sweep_event.point)


@given(strategies.nested_sweep_events, strategies.points)
def test_alternatives(sweep_event: SweepEvent, point: Point) -> None:
    assert sweep_event.is_above(point) or sweep_event.is_below(point)
