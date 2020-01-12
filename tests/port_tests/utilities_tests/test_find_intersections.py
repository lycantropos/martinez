from typing import Tuple

from hypothesis import given

from martinez.point import Point
from martinez.segment import Segment
from martinez.utilities import find_intersections
from tests.utils import implication
from . import strategies


@given(strategies.segments_pairs)
def test_basic(segments_pair: Tuple[Segment, Segment]) -> None:
    first_segment, second_segment = segments_pair

    result = find_intersections(first_segment, second_segment)

    assert isinstance(result, tuple)
    assert isinstance(result[0], int)
    assert all(coordinate is None or isinstance(coordinate, Point)
               for coordinate in result[1:])


@given(strategies.segments)
def test_same_segment(segment: Segment) -> None:
    result = find_intersections(segment, segment)

    assert result[0] == (1 if segment.is_degenerate else 2)
    assert result[1] == segment.source
    assert implication(segment.is_degenerate, result[-1] is None)


@given(strategies.segments)
def test_reversed(segment: Segment) -> None:
    result = find_intersections(segment, segment.reversed)

    assert result[0] == (1 if segment.is_degenerate else 2)
    assert result[1] == segment.source
    assert implication(segment.is_degenerate, result[-1] is None)
