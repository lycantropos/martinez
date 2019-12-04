import copy

from hypothesis import given

from martinez.contour import Contour
from . import strategies


@given(strategies.contours)
def test_shallow(contour: Contour) -> None:
    result = copy.copy(contour)

    assert result is not contour
    assert result == contour
    assert result.points is contour.points
    assert result.holes is contour.holes


@given(strategies.contours)
def test_deep(contour: Contour) -> None:
    result = copy.deepcopy(contour)

    assert result is not contour
    assert result == contour
    assert result.points is not contour.points
    assert result.holes is not contour.holes
