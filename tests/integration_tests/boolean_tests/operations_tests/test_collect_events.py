from typing import (List,
                    Tuple)

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from tests.integration_tests.utils import (
    are_bound_ported_sweep_events_lists_equal)
from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.nested_sweep_events_lists_pairs)
def test_basic(events_lists_pair: Tuple[List[BoundSweepEvent],
                                        List[PortedSweepEvent]]) -> None:
    bound_events, ported_events = events_lists_pair

    bound_result = BoundOperation.collect_events(bound_events)
    ported_result = PortedOperation.collect_events(ported_events)

    assert are_bound_ported_sweep_events_lists_equal(bound_result,
                                                     ported_result)
