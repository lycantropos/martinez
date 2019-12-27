from typing import (List,
                    Tuple)

from _martinez import (Operation as Bound,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from . import strategies


@given(strategies
       .non_empty_sweep_events_lists_pairs_with_indices_and_booleans_lists)
def test_basic(events_pair_with_position_and_processed
               : Tuple[Tuple[List[BoundSweepEvent], List[PortedSweepEvent]],
                       int, List[bool]]
               ) -> None:
    ((bound_events, ported_events),
     position, processed) = events_pair_with_position_and_processed

    bound_result = Bound.to_next_position(position, bound_events, processed)
    ported_result = Ported.to_next_position(position, ported_events, processed)

    assert bound_result == ported_result
