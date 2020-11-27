import copy

from hypothesis import given

from tests.bind_tests.hints import BoundContour as Contour
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
