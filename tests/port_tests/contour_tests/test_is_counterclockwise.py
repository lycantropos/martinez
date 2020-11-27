from hypothesis import given

from tests.port_tests.hints import PortedContour
from tests.utils import implication
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    result = contour.is_counterclockwise

    assert isinstance(result, bool)


@given(strategies.contours)
def test_empty(contour: PortedContour) -> None:
    assert implication(not contour.points, contour.is_counterclockwise)


@given(strategies.contours)
def test_reversed(contour: PortedContour) -> None:
    reversed_contour = PortedContour(contour.points[::-1], contour.holes,
                                     contour.is_external)

    assert implication(bool(contour.points),
                       contour.is_counterclockwise is not reversed_contour)
