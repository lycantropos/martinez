from typing import Tuple

from _martinez import SweepLineKey as Bound
from hypothesis import given

from martinez.boolean import SweepLineKey as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.sweep_line_keys_pairs, strategies.sweep_line_keys_pairs)
def test_basic(first_sweep_line_keys_pair: Tuple[Bound, Ported],
               second_sweep_line_keys_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_sweep_line_keys_pair
    second_bound, second_ported = second_sweep_line_keys_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
