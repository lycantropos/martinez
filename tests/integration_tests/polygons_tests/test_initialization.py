from typing import (List,
                    Tuple)

from _martinez import (Contour as BoundContour,
                       Polygon as Bound)
from hypothesis import given

from martinez.contour import Contour as PortedContour
from martinez.polygon import Polygon as Ported
from tests.utils import are_bound_ported_polygons_equal
from . import strategies


@given(strategies.bound_with_ported_contours_lists_pairs)
def test_basic(
        bound_with_ported_contours_lists_pair: Tuple[List[BoundContour],
                                                     List[PortedContour]]
) -> None:
    bound_contours, ported_contours = bound_with_ported_contours_lists_pair

    bound, ported = Bound(bound_contours), Ported(ported_contours)

    assert are_bound_ported_polygons_equal(bound, ported)
