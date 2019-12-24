from typing import (List,
                    Tuple)

from _martinez import (Operation as Bound,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from tests.utils import are_bound_ported_sweep_events_lists_equal
from . import strategies


@given(strategies.nested_sweep_events_lists_pairs)
def test_basic(events_lists_pair: Tuple[List[BoundSweepEvent],
                                        List[PortedSweepEvent]]) -> None:
    bound_events, ported_events = events_lists_pair

    bound_result = Bound.collect_events(bound_events)
    ported_result = Ported.collect_events(ported_events)

    assert are_bound_ported_sweep_events_lists_equal(bound_result,
                                                     ported_result)
