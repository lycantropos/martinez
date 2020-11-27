from typing import Tuple

from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedPoint,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_with_double_nested_sweep_events_and_points)
def test_basic(operation_with_event_and_point: Tuple[PortedOperation,
                                                     PortedSweepEvent,
                                                     PortedPoint]) -> None:
    operation, event, point = operation_with_event_and_point

    result = operation.divide_segment(event, point)

    assert result is None


@given(strategies.operations_with_double_nested_sweep_events_and_points)
def test_events(operation_with_event_and_point: Tuple[PortedOperation,
                                                      PortedSweepEvent,
                                                      PortedPoint]) -> None:
    operation, event, point = operation_with_event_and_point

    events_before = operation.events

    operation.divide_segment(event, point)

    events_after = operation.events

    assert isinstance(events_before, list)
    assert isinstance(events_after, list)
    assert not events_before
    assert len(events_after) == 2
    assert all(isinstance(event, PortedSweepEvent) for event in events_after)
