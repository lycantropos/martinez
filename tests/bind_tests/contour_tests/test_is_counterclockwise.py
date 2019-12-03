from _martinez import Contour
from hypothesis import given

from tests.utils import implication
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.is_counterclockwise

    assert isinstance(result, bool)


@given(strategies.contours)
def test_empty(contour: Contour) -> None:
    assert implication(not contour.points, contour.is_counterclockwise)


@given(strategies.contours)
def test_reversed(contour: Contour) -> None:
    reversed_contour = Contour(contour.points[::-1], contour.holes,
                               contour.is_external)

    assert implication(bool(contour.points),
                       contour.is_counterclockwise is not reversed_contour)
