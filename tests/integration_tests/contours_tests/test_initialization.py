from typing import (List,
                    Tuple)

from hypothesis import given

from tests.bind_tests.hints import (BoundContour,
                                    BoundPoint)
from tests.integration_tests.utils import are_bound_ported_contours_equal
from tests.port_tests.hints import (PortedContour,
                                    PortedPoint)
from . import strategies


@given(strategies.points_lists_pairs, strategies.non_negative_integers_lists,
       strategies.booleans)
def test_basic(points_lists_pair: Tuple[List[BoundPoint], List[PortedPoint]],
               holes: List[int],
               is_external: bool) -> None:
    bound_points, ported_points = points_lists_pair

    bound, ported = (BoundContour(bound_points, holes, is_external),
                     PortedContour(ported_points, holes, is_external))

    assert are_bound_ported_contours_equal(bound, ported)
