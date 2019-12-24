from typing import Tuple

from _martinez import (Operation as Bound,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from . import strategies


@given(strategies.operations_pairs,
       strategies.sweep_events_pairs)
def test_basic(operations_pair: Tuple[Bound, Ported],
               events_pair: Tuple[BoundSweepEvent, PortedSweepEvent]) -> None:
    bound, ported = operations_pair
    bound_event, ported_event = events_pair

    assert bound.in_result(bound_event) is ported.in_result(ported_event)
