from hypothesis import given

from tests.bind_tests.hints import BoundContour as Contour
from tests.utils import implication
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.is_clockwise

    assert isinstance(result, bool)


@given(strategies.contours)
def test_empty(contour: Contour) -> None:
    assert implication(not contour.points, not contour.is_clockwise)


@given(strategies.contours)
def test_reversed(contour: Contour) -> None:
    reversed_contour = Contour(contour.points[::-1], contour.holes,
                               contour.is_external)

    assert implication(bool(contour.points),
                       contour.is_clockwise is not reversed_contour)


@given(strategies.contours)
def test_alternatives(contour: Contour) -> None:
    assert implication(contour.is_clockwise, not contour.is_counterclockwise)
