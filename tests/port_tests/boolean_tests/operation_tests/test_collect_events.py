from typing import List

from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.nested_sweep_events_lists)
def test_basic(events: List[PortedSweepEvent]) -> None:
    result = PortedOperation.collect_events(events)

    assert isinstance(result, list)
    assert all(isinstance(element, PortedSweepEvent) for element in result)
