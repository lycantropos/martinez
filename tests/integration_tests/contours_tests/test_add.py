from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundContour,
                                    BoundPoint)
from tests.integration_tests.utils import are_bound_ported_contours_equal
from tests.port_tests.hints import (PortedContour,
                                    PortedPoint)
from . import strategies


@given(strategies.contours_pairs, strategies.points_pairs)
def test_basic(contours_pair: Tuple[BoundContour, PortedContour],
               points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = contours_pair
    bound_point, ported_point = points_pair

    bound.add(bound_point)
    ported.add(ported_point)

    assert are_bound_ported_contours_equal(bound, ported)
