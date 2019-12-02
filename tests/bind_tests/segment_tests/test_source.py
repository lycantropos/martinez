from _martinez import (Point,
                       Segment)
from hypothesis import given

from . import strategies


@given(strategies.segments, strategies.points)
def test_setting(segment: Segment, source: Point) -> None:
    segment.source = source

    assert segment.source == source
