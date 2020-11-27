from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundPoint,
                                    BoundSweepEvent)
from tests.integration_tests.utils import (
    are_bound_ported_operations_equal,
    are_bound_ported_sweep_events_lists_equal)
from tests.port_tests.hints import (PortedOperation,
                                    PortedPoint,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.operations_pairs,
       strategies.double_nested_sweep_events_pairs,
       strategies.points_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation],
               sweep_events_pair: Tuple[BoundSweepEvent, PortedSweepEvent],
               points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = operations_pair
    bound_event, ported_event = sweep_events_pair
    bound_point, ported_point = points_pair

    bound.divide_segment(bound_event, bound_point)
    ported.divide_segment(ported_event, ported_point)

    assert are_bound_ported_operations_equal(bound, ported)
    assert are_bound_ported_sweep_events_lists_equal(bound.events,
                                                     ported.events)
