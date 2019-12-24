from typing import Tuple

from _martinez import Segment as Bound
from hypothesis import given

from martinez.segment import Segment as Ported
from tests.utils import (are_bound_ported_segments_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.segments_pairs)
def test_round_trip(segments_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = segments_pair

    assert are_bound_ported_segments_equal(pickle_round_trip(bound),
                                           pickle_round_trip(ported))
