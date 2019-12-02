from _martinez import Point
from hypothesis import given

from . import strategies


@given(strategies.floats, strategies.floats)
def test_basic(x: float, y: float) -> None:
    result = Point(x, y)

    assert result.x == x
    assert result.y == y
