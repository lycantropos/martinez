from hypothesis import given

from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours, strategies.non_negative_integers)
def test_basic(contour: PortedContour, hole: int) -> None:
    result = contour.add_hole(hole)

    assert result is None


@given(strategies.contours, strategies.non_negative_integers)
def test_properties(contour: PortedContour, hole: int) -> None:
    contour.add_hole(hole)

    assert len(contour.holes) > 0
    assert contour.holes[-1] == hole
