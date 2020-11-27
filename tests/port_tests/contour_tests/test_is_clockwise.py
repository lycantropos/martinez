from hypothesis import given

from tests.port_tests.hints import PortedContour
from tests.utils import implication
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    result = contour.is_clockwise

    assert isinstance(result, bool)


@given(strategies.contours)
def test_empty(contour: PortedContour) -> None:
    assert implication(not contour.points, not contour.is_clockwise)


@given(strategies.contours)
def test_reversed(contour: PortedContour) -> None:
    reversed_contour = PortedContour(contour.points[::-1], contour.holes,
                                     contour.is_external)

    assert implication(bool(contour.points),
                       contour.is_clockwise is not reversed_contour)


@given(strategies.contours)
def test_alternatives(contour: PortedContour) -> None:
    assert implication(contour.is_clockwise, not contour.is_counterclockwise)
