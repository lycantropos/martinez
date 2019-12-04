import copy

from _martinez import Contour
from hypothesis import given

from . import strategies


@given(strategies.contours)
def test_shallow(contour: Contour) -> None:
    result = copy.copy(contour)

    assert result is not contour
    assert result == contour


@given(strategies.contours)
def test_deep(contour: Contour) -> None:
    result = copy.deepcopy(contour)

    assert result is not contour
    assert result == contour
