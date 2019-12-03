from typing import Tuple

from _martinez import Segment as Bound
from hypothesis import given

from martinez.segment import Segment as Ported
from tests.utils import are_bound_ported_segments_equal
from . import strategies


@given(strategies.bound_with_ported_segments_pairs)
def test_basic(bound_with_ported_segments_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bound_with_ported_segments_pair

    assert are_bound_ported_segments_equal(bound.reversed, ported.reversed)
