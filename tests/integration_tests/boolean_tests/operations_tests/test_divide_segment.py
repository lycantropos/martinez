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


@given(strategies.bound_with_ported_operations_pairs,
       strategies.bound_with_ported_nested_sweep_events_pairs,
       strategies.bound_with_ported_points_pairs)
def test_basic(bound_with_ported_operations_pair: Tuple[Bound, Ported],
               bound_with_ported_sweep_events_pair: Tuple[BoundSweepEvent,
                                                          PortedSweepEvent],
               bound_with_ported_points_pair: Tuple[BoundPoint, PortedPoint],
               ) -> None:
    bound, ported = bound_with_ported_operations_pair
    bound_event, ported_event = bound_with_ported_sweep_events_pair
    bound_point, ported_point = bound_with_ported_points_pair

    bound.divide_segment(bound_event, bound_point)
    ported.divide_segment(ported_event, ported_point)

    assert are_bound_ported_operations_equal(bound, ported)
    assert are_bound_ported_sweep_events_lists_equal(bound.events,
                                                     ported.events)
