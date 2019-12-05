from typing import (List,
                    Tuple)

from _martinez import (Contour as BoundContour,
                       Polygon as BoundPolygon)
from hypothesis import strategies

from martinez.contour import Contour as PortedContour
from martinez.polygon import Polygon as PortedPolygon
from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_contours_pair,
                              to_bound_with_ported_points_pair,
                              unsigned_integers_lists)
from tests.utils import transpose

bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_points_lists_pairs = strategies.lists(
        bound_with_ported_points_pairs).map(transpose)
bound_with_ported_contours_pairs = strategies.builds(
        to_bound_with_ported_contours_pair,
        bound_with_ported_points_lists_pairs,
        unsigned_integers_lists,
        booleans)
bound_with_ported_contours_lists_pairs = strategies.lists(
        bound_with_ported_contours_pairs).map(transpose)


def to_bound_with_ported_polygons_pair(
        bound_with_ported_contours_lists_pair: Tuple[List[BoundContour],
                                                     List[PortedContour]]
) -> Tuple[BoundPolygon, PortedPolygon]:
    bound_contours, ported_contours = bound_with_ported_contours_lists_pair
    return BoundPolygon(bound_contours), PortedPolygon(ported_contours)


bound_with_ported_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        bound_with_ported_contours_lists_pairs)
