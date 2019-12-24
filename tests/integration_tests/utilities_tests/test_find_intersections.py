from typing import Tuple

from _martinez import (Segment as BoundSegment,
                       find_intersections as bound_find_intersections)
from hypothesis import given

from martinez.segment import Segment as PortedSegment
from martinez.utilities import find_intersections as ported_find_intersections
from tests.utils import are_bound_ported_points_sequences_equal
from . import strategies


@given(strategies.segments_pairs_pairs)
def test_basic(segments_pair_pair: Tuple[Tuple[PortedSegment, PortedSegment],
                                         Tuple[BoundSegment, BoundSegment]]
               ) -> None:
    bound_segments, ported_segments = segments_pair_pair

    bound_result = bound_find_intersections(*bound_segments)
    ported_result = ported_find_intersections(*ported_segments)

    bound_intersections_count = bound_result[0]
    ported_intersections_count = ported_result[0]
    assert bound_intersections_count == ported_intersections_count
    assert are_bound_ported_points_sequences_equal(
            bound_result[1:1 + bound_intersections_count],
            ported_result[1:1 + ported_intersections_count])
    assert (bound_result[1 + bound_intersections_count:]
            == ported_result[1 + ported_intersections_count:])
