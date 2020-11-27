from hypothesis import given

from martinez.bounding_box import BoundingBox
from martinez.contour import Contour
from tests.utils import (implication)
from ...integration_tests.utils import are_bounding_boxes_empty
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    assert isinstance(contour.bounding_box, BoundingBox)


@given(strategies.contours)
def test_empty(contour: Contour) -> None:
    assert implication(not contour.points,
                       are_bounding_boxes_empty(contour.bounding_box))
