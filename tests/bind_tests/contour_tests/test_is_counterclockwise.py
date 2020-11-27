from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.utils import implication
from . import strategies


@given(strategies.contours)
def test_basic(contour: BoundContour) -> None:
    result = contour.is_counterclockwise

    assert isinstance(result, bool)


@given(strategies.contours)
def test_empty(contour: BoundContour) -> None:
    assert implication(not contour.points, contour.is_counterclockwise)


@given(strategies.contours)
def test_reversed(contour: BoundContour) -> None:
    reversed_contour = BoundContour(contour.points[::-1], contour.holes,
                                    contour.is_external)

    assert implication(bool(contour.points),
                       contour.is_counterclockwise is not reversed_contour)
