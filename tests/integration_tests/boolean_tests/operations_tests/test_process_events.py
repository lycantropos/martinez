from typing import (List,
                    Tuple)

from _martinez import (Operation as Bound,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from tests.utils import (are_bound_ported_polygons_equal,
                         are_bound_ported_sweep_events_lists_equal)
from . import strategies


@given(strategies.operations_with_events_lists_pairs)
def test_basic(
        operations_with_events_lists_pair: Tuple[Tuple[Bound, Ported],
                                                 Tuple[List[BoundSweepEvent],
                                                       List[PortedSweepEvent]]]
) -> None:
    ((bound, ported),
     (bound_events, ported_events)) = operations_with_events_lists_pair

    bound.process_events(bound_events)
    ported.process_events(ported_events)

    assert are_bound_ported_sweep_events_lists_equal(bound_events,
                                                     ported_events)
    assert are_bound_ported_polygons_equal(bound.resultant, ported.resultant)
