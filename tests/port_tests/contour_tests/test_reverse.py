from copy import deepcopy

from hypothesis import given

from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    result = contour.reverse()

    assert result is None


@given(strategies.contours)
def test_involution(contour: PortedContour) -> None:
    original = deepcopy(contour)

    contour.reverse()
    contour.reverse()

    assert contour == original
