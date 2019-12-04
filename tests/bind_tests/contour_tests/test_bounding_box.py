from _martinez import (BoundingBox,
                       Contour)
from hypothesis import given

from tests.utils import (implication,
                         is_bounding_box_empty)
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    assert isinstance(contour.bounding_box, BoundingBox)


@given(strategies.contours)
def test_empty(contour: Contour) -> None:
    assert implication(not contour.points,
                       is_bounding_box_empty(contour.bounding_box))
