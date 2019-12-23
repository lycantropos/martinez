from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from . import strategies


@given(strategies.operations, strategies.sweep_events)
def test_basic(operation: Operation, event: SweepEvent) -> None:
    assert isinstance(operation.in_result(event), bool)
