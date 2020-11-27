from hypothesis import given

from tests.bind_tests.hints import (BoundBoundingBox,
                                    BoundContour)
from tests.utils import (are_bounding_boxes_empty,
                         implication)
from . import strategies


@given(strategies.contours)
def test_basic(contour: BoundContour) -> None:
    assert isinstance(contour.bounding_box, BoundBoundingBox)


@given(strategies.contours)
def test_empty(contour: BoundContour) -> None:
    assert implication(not contour.points,
                       are_bounding_boxes_empty(contour.bounding_box))
