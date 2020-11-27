from _martinez import (BoundingBox,
                       Polygon)
from hypothesis import given

from tests.utils import (implication)
from ...integration_tests.utils import are_bounding_boxes_empty
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: Polygon) -> None:
    assert isinstance(polygon.bounding_box, BoundingBox)


@given(strategies.polygons)
def test_empty(polygon: Polygon) -> None:
    assert implication(not polygon.contours,
                       are_bounding_boxes_empty(polygon.bounding_box))
