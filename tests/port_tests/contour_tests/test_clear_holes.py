from hypothesis import given

from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    result = contour.clear_holes()

    assert result is None


@given(strategies.contours)
def test_properties(contour: PortedContour) -> None:
    contour.clear_holes()

    assert not contour.holes
