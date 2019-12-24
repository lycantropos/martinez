from typing import Tuple

from _martinez import (Point as BoundPoint,
                       SweepEvent as Bound)
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from martinez.point import Point as PortedPoint
from . import strategies


@given(strategies.nested_sweep_events_pairs,
       strategies.points_pairs)
def test_basic(sweep_events_pair: Tuple[Bound, Ported],
               points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = sweep_events_pair
    bound_point, ported_point = points_pair

    assert bound.is_above(bound_point) is ported.is_above(ported_point)
