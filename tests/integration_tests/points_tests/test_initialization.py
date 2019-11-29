from _martinez import Point_2
from hypothesis import given

from martinez.point import Point
from tests import strategies


@given(strategies.floats, strategies.floats)
def test_basic(x: float, y: float) -> None:
    source, target = Point_2(x, y), Point(x, y)

    assert source.x == target.x
    assert source.y == target.y
