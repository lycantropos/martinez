from hypothesis import given

from tests.bind_tests.hints import BoundSegment as BoundSegment
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.segments)
def test_reflexivity(segment: BoundSegment) -> None:
    assert segment == segment


@given(strategies.segments, strategies.segments)
def test_symmetry(first_segment: BoundSegment,
                  second_segment: BoundSegment) -> None:
    assert equivalence(first_segment == second_segment,
                       second_segment == first_segment)


@given(strategies.segments, strategies.segments, strategies.segments)
def test_transitivity(first_segment: BoundSegment,
                      second_segment: BoundSegment,
                      third_segment: BoundSegment) -> None:
    assert implication(first_segment == second_segment
                       and second_segment == third_segment,
                       first_segment == third_segment)


@given(strategies.segments, strategies.segments)
def test_connection_with_inequality(first_segment: BoundSegment,
                                    second_segment: BoundSegment) -> None:
    assert equivalence(not first_segment == second_segment,
                       first_segment != second_segment)
