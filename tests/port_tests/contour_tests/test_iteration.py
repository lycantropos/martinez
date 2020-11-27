from hypothesis import given

from tests.port_tests.hints import (PortedContour,
                                    PortedPoint)
from tests.utils import capacity
from . import strategies


@given(strategies.contours)
def test_basic(contour: PortedContour) -> None:
    result = iter(contour)

    assert all(isinstance(element, PortedPoint) for element in result)


@given(strategies.contours)
def test_elements(contour: PortedContour) -> None:
    result = iter(contour)

    assert all(element in contour.points for element in result)


@given(strategies.contours)
def test_size(contour: PortedContour) -> None:
    result = iter(contour)

    assert capacity(result) == len(contour.points)
