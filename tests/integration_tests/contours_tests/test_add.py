from typing import Tuple

from _martinez import (Contour as Bound,
                       Point as BoundPoint)
from hypothesis import given

from martinez.contour import Contour as Ported
from martinez.point import Point as PortedPoint
from ..utils import are_bound_ported_contours_equal
from . import strategies


@given(strategies.contours_pairs, strategies.points_pairs)
def test_basic(contours_pair: Tuple[Bound, Ported],
               points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = contours_pair
    bound_point, ported_point = points_pair

    bound.add(bound_point)
    ported.add(ported_point)

    assert are_bound_ported_contours_equal(bound, ported)
