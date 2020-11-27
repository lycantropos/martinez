from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPoint
from tests.integration_tests.utils import are_bound_ported_bounding_boxes_equal
from tests.port_tests.hints import PortedPoint
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = points_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
