from typing import Tuple

from _martinez import Operation as Bound
from hypothesis import given

from martinez.boolean import Operation as Ported
from ...utils import are_bound_ported_sweep_events_lists_equal
from . import strategies


@given(strategies.pre_processed_non_trivial_operations_pairs)
def test_basic(operations_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = operations_pair

    bound_result = bound.sweep()
    ported_result = ported.sweep()

    assert are_bound_ported_sweep_events_lists_equal(bound_result,
                                                     ported_result)
