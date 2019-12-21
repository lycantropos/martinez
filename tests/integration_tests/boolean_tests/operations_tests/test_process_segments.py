from typing import Tuple

from _martinez import Operation as Bound
from hypothesis import given

from martinez.boolean import Operation as Ported
from tests.utils import (are_bound_ported_operations_equal,
                         are_bound_ported_sweep_events_lists_equal)
from . import strategies


@given(strategies.bound_with_ported_operations_pairs)
def test_basic(bound_with_ported_operations_pair: Tuple[Bound, Ported]
               ) -> None:
    bound, ported = bound_with_ported_operations_pair

    bound.process_segments()
    ported.process_segments()

    assert are_bound_ported_operations_equal(bound, ported)
    assert are_bound_ported_sweep_events_lists_equal(bound.events,
                                                     ported.events)
