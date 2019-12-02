from _martinez import (Point,
                       Segment)
from hypothesis import given

from . import strategies


@given(strategies.segments)
def test_basic(segment: Segment) -> None:
    result = segment.max

    assert isinstance(result, Point)
    assert result == segment.source or result == segment.target
