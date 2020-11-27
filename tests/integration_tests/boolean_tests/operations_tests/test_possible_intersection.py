from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_pairs, strategies.nested_sweep_events_pairs_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation],
               events_pair_pair: Tuple[Tuple[BoundSweepEvent,
                                             BoundSweepEvent],
                                       Tuple[PortedSweepEvent,
                                             PortedSweepEvent]]) -> None:
    bound, ported = operations_pair
    bound_events_pair, ported_events_pair = events_pair_pair
    first_bound_event, second_bound_event = bound_events_pair
    first_ported_event, second_ported_event = ported_events_pair

    bound_result = bound.possible_intersection(first_bound_event,
                                               second_bound_event)
    ported_result = ported.possible_intersection(first_ported_event,
                                                 second_ported_event)

    assert bound_result == ported_result
