from hypothesis import given

from tests.port_tests.hints import (PortedBoundingBox,
                                    PortedContour)
from tests.utils import (are_bounding_boxes_empty,
                         implication)
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    assert isinstance(contour.bounding_box, PortedBoundingBox)


@given(strategies.contours)
def test_empty(contour: PortedContour) -> None:
    assert implication(not contour.points,
                       are_bounding_boxes_empty(contour.bounding_box))
