from hypothesis import given

from tests.port_tests.hints import PortedBoundingBox, PortedPolygon
from tests.utils import (are_bounding_boxes_empty, implication)
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: PortedPolygon) -> None:
    assert isinstance(polygon.bounding_box, PortedBoundingBox)


@given(strategies.polygons)
def test_empty(polygon: PortedPolygon) -> None:
    assert implication(not polygon.contours,
                       are_bounding_boxes_empty(polygon.bounding_box))
