from typing import Tuple

import pytest
from hypothesis import given

from tests.port_tests.hints import (PortedPoint,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.leaf_sweep_events_with_points)
def test_leaf(event_with_point: Tuple[PortedSweepEvent, PortedPoint]) -> None:
    event, point = event_with_point

    with pytest.raises(ValueError):
        event.is_above(point)


@given(strategies.nested_sweep_events_with_points)
def test_nested(event_with_point: Tuple[PortedSweepEvent, PortedPoint]
                ) -> None:
    event, point = event_with_point

    result = event.is_above(point)

    assert isinstance(result, bool)


@given(strategies.nested_sweep_events)
def test_self_point(event: PortedSweepEvent) -> None:
    assert event.is_above(event.point)


@given(strategies.nested_sweep_events_with_points)
def test_alternatives(event_with_point: Tuple[PortedSweepEvent, PortedPoint]
                      ) -> None:
    event, point = event_with_point

    assert event.is_above(point) or event.is_below(point)
