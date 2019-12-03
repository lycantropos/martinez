from typing import (List,
                    Tuple)

from _martinez import (Contour as Bound,
                       Point as BoundPoint)
from hypothesis import given

from martinez.contour import Contour as Ported
from martinez.point import Point as PortedPoint
from tests.utils import are_bound_ported_list_points_equal
from . import strategies


@given(strategies.bound_with_ported_points_lists_pairs,
       strategies.non_negative_integers_lists,
       strategies.booleans)
def test_basic(bound_with_ported_points_lists_pair: Tuple[List[BoundPoint],
                                                          List[PortedPoint]],
               holes: List[int],
               is_external: bool) -> None:
    bound_points, ported_points = bound_with_ported_points_lists_pair

    bound, ported = (Bound(bound_points, holes, is_external),
                     Ported(ported_points, holes, is_external))

    assert are_bound_ported_list_points_equal(bound.points, ported.points)
    assert bound.holes == ported.holes
    assert bound.is_external == ported.is_external
