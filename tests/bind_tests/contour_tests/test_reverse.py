from copy import deepcopy

from hypothesis import given

from tests.bind_tests.hints import BoundContour as Contour
from . import strategies


@given(strategies.contours)
def test_basic(contour: Contour) -> None:
    result = contour.reverse()

    assert result is None


@given(strategies.contours)
def test_involution(contour: Contour) -> None:
    original = deepcopy(contour)

    contour.reverse()
    contour.reverse()

    assert contour == original
