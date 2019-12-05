from typing import (List,
                    Tuple)

from _martinez import (Contour as Bound,
                       Point as BoundPoint)
from hypothesis import strategies

from martinez.contour import Contour as Ported
from martinez.point import Point as PortedPoint
from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_points_pair,
                              unsigned_integers,
                              unsigned_integers_lists)
from tests.utils import transpose

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_points_lists_pairs = strategies.lists(
        bound_with_ported_points_pairs).map(transpose)


def to_bound_with_ported_contours_pair(
        bound_with_ported_points_lists_pair: Tuple[List[BoundPoint],
                                                   List[PortedPoint]],
        holes: List[int],
        is_external: bool) -> Tuple[Bound, Ported]:
    bound_points, ported_points = bound_with_ported_points_lists_pair
    return (Bound(bound_points, holes, is_external),
            Ported(ported_points, holes, is_external))


bound_with_ported_contours_pairs = strategies.builds(
        to_bound_with_ported_contours_pair,
        bound_with_ported_points_lists_pairs,
        non_negative_integers_lists,
        booleans)
