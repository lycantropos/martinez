from typing import Tuple

from _martinez import (Point as BoundPoint,
                       SweepEvent as Bound)
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from martinez.point import Point as PortedPoint
from . import strategies


@given(strategies.bound_with_ported_nested_sweep_events_pairs,
       strategies.bound_with_ported_points_pairs)
def test_basic(bound_with_ported_sweep_events_pair: Tuple[Bound, Ported],
               bound_with_ported_points_pair: Tuple[BoundPoint, PortedPoint],
               ) -> None:
    bound, ported = bound_with_ported_sweep_events_pair
    bound_point, ported_point = bound_with_ported_points_pair

    assert bound.is_below(bound_point) is ported.is_below(ported_point)
