from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from tests.integration_tests.utils import are_bound_ported_bounding_boxes_equal
from tests.port_tests.hints import PortedPolygon
from . import strategies


@given(strategies.polygons_pairs)
def test_basic(polygons_pair: Tuple[BoundPolygon, PortedPolygon]) -> None:
    bound, ported = polygons_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
