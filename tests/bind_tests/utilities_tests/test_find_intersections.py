from _martinez import find_intersections
from hypothesis import given

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSegment)
from tests.utils import implication
from . import strategies


@given(strategies.segments, strategies.segments)
def test_basic(first_segment: BoundSegment,
               second_segment: BoundSegment) -> None:
    result = find_intersections(first_segment, second_segment)

    assert isinstance(result, tuple)
    assert isinstance(result[0], int)
    assert all(coordinate is None or isinstance(coordinate, BoundPoint)
               for coordinate in result[1:])


@given(strategies.segments)
def test_same_segment(segment: BoundSegment) -> None:
    result = find_intersections(segment, segment)

    assert result[0] == (1 if segment.is_degenerate else 2)
    assert result[1] == segment.source
    assert implication(segment.is_degenerate, result[-1] is None)


@given(strategies.segments)
def test_reversed(segment: BoundSegment) -> None:
    result = find_intersections(segment, segment.reversed)

    assert result[0] == (1 if segment.is_degenerate else 2)
    assert result[1] == segment.source
    assert implication(segment.is_degenerate, result[-1] is None)
