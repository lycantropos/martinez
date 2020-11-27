from typing import Tuple

from hypothesis import given

from tests.port_tests.hints import PortedSegment
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.segments)
def test_reflexivity(segment: PortedSegment) -> None:
    assert segment == segment


@given(strategies.segments_pairs)
def test_symmetry(segments_pair: Tuple[PortedSegment, PortedSegment]) -> None:
    first_segment, second_segment = segments_pair

    assert equivalence(first_segment == second_segment,
                       second_segment == first_segment)


@given(strategies.segments_triplets)
def test_transitivity(segments_triplet: Tuple[PortedSegment, PortedSegment,
                                              PortedSegment]) -> None:
    first_segment, second_segment, third_segment = segments_triplet

    assert implication(first_segment == second_segment
                       and second_segment == third_segment,
                       first_segment == third_segment)


@given(strategies.segments_pairs)
def test_connection_with_inequality(segments_pair: Tuple[PortedSegment,
                                                         PortedSegment]
                                    ) -> None:
    first_segment, second_segment = segments_pair

    assert equivalence(not first_segment == second_segment,
                       first_segment != second_segment)
