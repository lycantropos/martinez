from typing import (Optional,
                    Tuple)

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from tests.integration_tests.utils import are_bound_ported_sweep_events_equal
from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_pairs, strategies.sweep_events_pairs,
       strategies.maybe_nested_sweep_events_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation],
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
