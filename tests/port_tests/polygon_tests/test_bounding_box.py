from hypothesis import given

from martinez.bounding_box import BoundingBox
from martinez.polygon import Polygon
from tests.utils import (implication,
                         is_bounding_box_empty)
from . import strategies


@given(strategies.polygons)
def test_basic(polygon: Polygon) -> None:
    assert isinstance(polygon.bounding_box, BoundingBox)


@given(strategies.polygons)
def test_empty(polygon: Polygon) -> None:
    assert implication(not polygon.contours,
                       is_bounding_box_empty(polygon.bounding_box))
