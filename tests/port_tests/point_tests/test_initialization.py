from typing import Tuple

from hypothesis import given

from martinez.hints import Scalar
from martinez.point import Point
from . import strategies


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    x, y = scalars_pair

    result = Point(x, y)

    assert result.x == x
    assert result.y == y
