from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.operations, strategies.sweep_events)
def test_basic(operation: BoundOperation, event: BoundSweepEvent) -> None:
    assert isinstance(operation.in_result(event), bool)
