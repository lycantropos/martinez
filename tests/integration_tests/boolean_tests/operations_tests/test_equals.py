from typing import Tuple

from _martinez import Operation as Bound
from hypothesis import given

from martinez.boolean import Operation as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.operations_pairs, strategies.operations_pairs)
def test_basic(first_operations_pair: Tuple[Bound, Ported],
               second_operations_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_operations_pair
    second_bound, second_ported = second_operations_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
