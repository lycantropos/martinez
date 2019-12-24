from typing import Tuple

from _martinez import Segment as Bound
from hypothesis import given

from martinez.segment import Segment as Ported
from tests.utils import are_bound_ported_points_equal
from . import strategies


@given(strategies.segments_pairs)
def test_basic(segments_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = segments_pair

    assert are_bound_ported_points_equal(bound.max, ported.max)
