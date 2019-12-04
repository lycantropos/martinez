import copy

from hypothesis import given

from martinez.point import Point
from . import strategies


@given(strategies.points)
def test_shallow(point: Point) -> None:
    result = copy.copy(point)

    assert result is not point
    assert result == point


@given(strategies.points)
def test_deep(point: Point) -> None:
    result = copy.deepcopy(point)

    assert result is not point
    assert result == point
