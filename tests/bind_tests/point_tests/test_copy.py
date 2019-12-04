import copy

from _martinez import Point
from hypothesis import given

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
