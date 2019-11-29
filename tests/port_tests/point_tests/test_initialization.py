from hypothesis import given

from martinez.point import Point
from tests import strategies


@given(strategies.literals.scalars, strategies.scalars)
def test_basic(x: float, y: float) -> None:
    result = Point(x, y)

    assert result.x == x
    assert result.y == y
