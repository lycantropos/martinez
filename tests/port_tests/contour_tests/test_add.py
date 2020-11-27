from hypothesis import given

from tests.port_tests.hints import (PortedContour,
                                    PortedPoint)
from . import strategies


@given(strategies.contours, strategies.points)
def test_basic(contour: PortedContour, point: PortedPoint) -> None:
    result = contour.add(point)

    assert result is None


@given(strategies.contours, strategies.points)
def test_properties(contour: PortedContour, point: PortedPoint) -> None:
    contour.add(point)

    assert len(contour.points) > 0
    assert contour.points[-1] == point
