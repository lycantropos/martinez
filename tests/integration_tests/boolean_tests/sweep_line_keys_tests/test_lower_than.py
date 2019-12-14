from typing import Tuple

from _martinez import SweepLineKey as Bound
from hypothesis import given

from martinez.boolean import SweepLineKey as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.bound_with_ported_nested_sweep_line_keys_pairs,
       strategies.bound_with_ported_nested_sweep_line_keys_pairs)
def test_basic(first_bound_with_ported_sweep_line_keys_pair: Tuple[Bound,
                                                                   Ported],
               second_bound_with_ported_sweep_line_keys_pair: Tuple[Bound,
                                                                    Ported]
               ) -> None:
    first_bound, first_ported = first_bound_with_ported_sweep_line_keys_pair
    second_bound, second_ported = second_bound_with_ported_sweep_line_keys_pair

    assert equivalence(first_bound < second_bound,
                       first_ported < second_ported)
