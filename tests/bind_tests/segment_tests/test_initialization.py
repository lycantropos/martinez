from _martinez import (Point,
                       Segment)
from hypothesis import given

from . import strategies


@given(strategies.points, strategies.points)
def test_basic(source: Point, target: Point) -> None:
    result = Segment(source, target)

    assert result.source == source
    assert result.target == target
