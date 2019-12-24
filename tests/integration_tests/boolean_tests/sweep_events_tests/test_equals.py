from typing import Tuple

from _martinez import SweepEvent as Bound
from hypothesis import given

from martinez.boolean import SweepEvent as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.sweep_events_pairs, strategies.sweep_events_pairs)
def test_basic(first_sweep_events_pair: Tuple[Bound, Ported],
               second_sweep_events_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_sweep_events_pair
    second_bound, second_ported = second_sweep_events_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
