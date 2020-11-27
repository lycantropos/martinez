from hypothesis import given

from tests.bind_tests.hints import (BoundPoint, Contour)
from . import strategies


@given(strategies.contours, strategies.points)
def test_basic(contour: Contour, point: BoundPoint) -> None:
    result = contour.add(point)

    assert result is None


@given(strategies.contours, strategies.points)
def test_properties(contour: Contour, point: BoundPoint) -> None:
    contour.add(point)

    assert len(contour.points) > 0
    assert contour.points[-1] == point
