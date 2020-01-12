from typing import Tuple

from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from . import strategies


@given(strategies.operations_with_sweep_events)
def test_basic(operation_with_sweep_event: Tuple[Operation, SweepEvent]
               ) -> None:
    operation, event = operation_with_sweep_event

    assert isinstance(operation.in_result(event), bool)
