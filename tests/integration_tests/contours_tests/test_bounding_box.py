from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.integration_tests.utils import are_bound_ported_bounding_boxes_equal
from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours_pairs)
def test_basic(contours_pair: Tuple[BoundContour, PortedContour]) -> None:
    bound, ported = contours_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
