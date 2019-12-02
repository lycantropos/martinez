from _martinez import (Point,
                       Segment)
from hypothesis import given

from . import strategies


@given(strategies.segments, strategies.points)
def test_setting(segment: Segment, target: Point) -> None:
    segment.target = target

    assert segment.target == target
