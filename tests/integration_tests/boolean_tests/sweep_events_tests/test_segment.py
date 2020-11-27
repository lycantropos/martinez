from typing import Tuple

from _martinez import SweepEvent as Bound
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from ...utils import are_bound_ported_segments_equal
from . import strategies


@given(strategies.nested_sweep_events_pairs)
def test_basic(sweep_events_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = sweep_events_pair

    assert are_bound_ported_segments_equal(bound.segment, ported.segment)
