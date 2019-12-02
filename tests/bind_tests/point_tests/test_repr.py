import sys

from _martinez import Point
from hypothesis import given

from . import strategies


@given(strategies.points)
def test_basic(point: Point) -> None:
    result = repr(point)

    assert result.startswith(Point.__module__)
    assert Point.__qualname__ in result


@given(strategies.points)
def test_round_trip(point: Point) -> None:
    result = repr(point)

    assert eval(result, sys.modules) == point
