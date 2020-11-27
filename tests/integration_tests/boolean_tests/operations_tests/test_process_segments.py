from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.integration_tests.utils import (
    are_bound_ported_operations_equal,
    are_bound_ported_sweep_events_lists_equal)
from tests.port_tests.hints import PortedOperation
from . import strategies


@given(strategies.operations_pairs)
def test_basic(operations_pair: Tuple[BoundOperation, PortedOperation]
               ) -> None:
    bound, ported = operations_pair

    bound.process_segments()
    ported.process_segments()

    assert are_bound_ported_operations_equal(bound, ported)
    assert are_bound_ported_sweep_events_lists_equal(bound.events,
                                                     ported.events)
