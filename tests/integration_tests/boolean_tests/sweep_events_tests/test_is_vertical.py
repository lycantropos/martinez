from typing import Tuple

from _martinez import SweepEvent as Bound
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from . import strategies


@given(strategies.bound_with_ported_nested_sweep_events_pairs)
def test_basic(bound_with_ported_sweep_events_pair: Tuple[Bound, Ported]
               ) -> None:
    bound, ported = bound_with_ported_sweep_events_pair

    assert bound.is_vertical is ported.is_vertical
