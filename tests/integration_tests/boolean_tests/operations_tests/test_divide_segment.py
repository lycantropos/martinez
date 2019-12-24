from typing import Tuple

from _martinez import (Operation as Bound,
                       Point as BoundPoint,
                       SweepEvent as BoundSweepEvent)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              SweepEvent as PortedSweepEvent)
from martinez.point import Point as PortedPoint
from tests.utils import (are_bound_ported_operations_equal,
                         are_bound_ported_sweep_events_lists_equal)
from . import strategies


@given(strategies.operations_pairs,
       strategies.nested_sweep_events_pairs,
       strategies.points_pairs)
def test_basic(operations_pair: Tuple[Bound, Ported],
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
