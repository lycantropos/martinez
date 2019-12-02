from hypothesis import given

from martinez.point import Point
from martinez.segment import Segment
from . import strategies


@given(strategies.segments)
def test_basic(segment: Segment) -> None:
    result = segment.min

    assert isinstance(result, Point)
    assert result == segment.source or result == segment.target
