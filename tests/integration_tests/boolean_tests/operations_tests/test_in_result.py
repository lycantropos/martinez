from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_pairs,
       strategies.sweep_events_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation],
               events_pair: Tuple[BoundSweepEvent, PortedSweepEvent]) -> None:
    bound, ported = operations_pair
    bound_event, ported_event = events_pair

    assert bound.in_result(bound_event) is ported.in_result(ported_event)
