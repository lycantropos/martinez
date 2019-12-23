from typing import Tuple

from _martinez import (Operation as Bound,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from . import strategies


@given(strategies.bound_with_ported_operations_pairs,
       strategies.bound_with_ported_sweep_events_pairs)
def test_basic(bound_with_ported_operations_pair: Tuple[Bound, Ported],
               bound_with_ported_events_pair: Tuple[BoundSweepEvent,
                                                    PortedSweepEvent]) -> None:
    bound, ported = bound_with_ported_operations_pair
    bound_event, ported_event = bound_with_ported_events_pair

    assert bound.in_result(bound_event) is ported.in_result(ported_event)
