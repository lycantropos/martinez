from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from tests.port_tests.hints import PortedSegment
from tests.utils import equivalence
from . import strategies


@given(strategies.segments_pairs, strategies.segments_pairs)
def test_basic(first_segments_pair: Tuple[BoundSegment, PortedSegment],
               second_segments_pair: Tuple[BoundSegment, PortedSegment]
               ) -> None:
    first_bound, first_ported = first_segments_pair
    second_bound, second_ported = second_segments_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
