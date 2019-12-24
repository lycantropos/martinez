from typing import Tuple

from _martinez import Segment as Bound
from hypothesis import given

from martinez.segment import Segment as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.segments_pairs, strategies.segments_pairs)
def test_basic(first_segments_pair: Tuple[Bound, Ported],
               second_segments_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_segments_pair
    second_bound, second_ported = second_segments_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
