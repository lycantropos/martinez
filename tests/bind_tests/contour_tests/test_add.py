from _martinez import (Contour,
                       Point)
from hypothesis import given

from . import strategies


@given(strategies.contours, strategies.points)
def test_basic(contour: Contour, point: Point) -> None:
    result = contour.add(point)

    assert result is None


@given(strategies.contours, strategies.points)
def test_properties(contour: Contour, point: Point) -> None:
    contour.add(point)

    assert len(contour.points) > 0
    assert contour.points[-1] == point
