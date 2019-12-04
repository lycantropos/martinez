from _martinez import Contour
from hypothesis import given

from tests.utils import implication
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.reverse()

    assert result is None


@given(strategies.contours)
def test_orientation(contour: Contour) -> None:
    contour.set_clockwise()

    assert implication(len(contour.points) > 1, contour.is_clockwise)
