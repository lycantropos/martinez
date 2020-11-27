from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.integration_tests.utils import (
    are_bound_ported_sweep_events_lists_equal)
from tests.port_tests.hints import PortedOperation
from . import strategies


@given(strategies.pre_processed_non_trivial_operations_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation]
               ) -> None:
    bound, ported = operations_pair

    bound_result = bound.sweep()
    ported_result = ported.sweep()

    assert are_bound_ported_sweep_events_lists_equal(bound_result,
                                                     ported_result)
