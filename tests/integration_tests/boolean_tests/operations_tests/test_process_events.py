from typing import (List,
                    Tuple)

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from tests.integration_tests.utils import (
    are_bound_ported_polygons_equal,
    are_bound_ported_sweep_events_lists_equal)
from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_with_events_lists_pairs)
def test_basic(operations_with_events_lists_pair
               : Tuple[Tuple[BoundOperation, PortedOperation],
                       Tuple[List[BoundSweepEvent], List[PortedSweepEvent]]]
               ) -> None:
    ((bound, ported),
     (bound_events, ported_events)) = operations_with_events_lists_pair

    bound.process_events(bound_events)
    ported.process_events(ported_events)

    assert are_bound_ported_sweep_events_lists_equal(bound_events,
                                                     ported_events)
    assert are_bound_ported_polygons_equal(bound.resultant, ported.resultant)
