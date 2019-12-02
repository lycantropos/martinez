from typing import Tuple

from hypothesis import given

from martinez.point import Point
from martinez.segment import Segment
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[Point, Point]) -> None:
    source, target = points_pair

    result = Segment(source, target)

    assert result.source == source
    assert result.target == target
