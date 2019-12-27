from typing import (Optional,
                    Tuple)

from _martinez import (Operation as Bound,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from tests.utils import are_bound_ported_sweep_events_equal
from . import strategies


@given(strategies.operations_pairs, strategies.sweep_events_pairs,
       strategies.maybe_nested_sweep_events_pairs)
def test_basic(operations_pair: Tuple[Bound, Ported],
               events_pair: Tuple[BoundSweepEvent, PortedSweepEvent],
               previous_events_pair: Tuple[Optional[BoundSweepEvent],
                                           Optional[PortedSweepEvent]]
               ) -> None:
    bound, ported = operations_pair
    bound_event, ported_event = events_pair
    bound_previous_event, ported_previous_event = previous_events_pair

    bound.compute_fields(bound_event, bound_previous_event)
    ported.compute_fields(ported_event, ported_previous_event)

    assert are_bound_ported_sweep_events_equal(bound_event, ported_event)
