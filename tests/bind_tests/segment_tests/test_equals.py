from _martinez import Segment
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.segments)
def test_reflexivity(segment: Segment) -> None:
    assert segment == segment


@given(strategies.segments, strategies.segments)
def test_symmetry(first_segment: Segment, second_segment: Segment) -> None:
    assert equivalence(first_segment == second_segment,
                       second_segment == first_segment)


@given(strategies.segments, strategies.segments, strategies.segments)
def test_transitivity(first_segment: Segment,
                      second_segment: Segment,
                      third_segment: Segment) -> None:
    assert implication(first_segment == second_segment
                       and second_segment == third_segment,
                       first_segment == third_segment)


@given(strategies.segments, strategies.segments)
def test_connection_with_inequality(first_segment: Segment,
                                    second_segment: Segment) -> None:
    assert equivalence(not first_segment == second_segment,
                       first_segment != second_segment)
