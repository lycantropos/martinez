from copy import deepcopy

from _martinez import Contour
from hypothesis import given

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
