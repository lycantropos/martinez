from typing import Tuple

import pytest
from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations, strategies.nested_sweep_events_pairs)
def test_basic(operation: PortedOperation,
               events_pair: Tuple[PortedSweepEvent, PortedSweepEvent]) -> None:
    first_event, second_event = events_pair

    result = operation.possible_intersection(first_event, second_event)

    assert result in {0, 1, 2, 3}


@given(strategies.operations, strategies.non_degenerate_nested_sweep_events)
def test_same_event(operation: PortedOperation,
                    event: PortedSweepEvent) -> None:
    with pytest.raises(ValueError):
        operation.possible_intersection(event, event)
