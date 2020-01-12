from typing import Tuple

import pytest
from hypothesis import given

from martinez.boolean import SweepEvent
from martinez.point import Point
from . import strategies


@given(strategies.leaf_sweep_events_with_points)
def test_leaf(event_with_point: Tuple[SweepEvent, Point]) -> None:
    event, point = event_with_point

    with pytest.raises(ValueError):
        event.is_below(point)


@given(strategies.nested_sweep_events_with_points)
def test_nested(event_with_point: Tuple[SweepEvent, Point]) -> None:
    event, point = event_with_point

    result = event.is_below(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(event: SweepEvent) -> None:
    assert not event.is_below(event.point)
