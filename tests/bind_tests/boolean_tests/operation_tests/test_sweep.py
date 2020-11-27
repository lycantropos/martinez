from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.pre_processed_non_trivial_operations)
def test_basic(operation: BoundOperation) -> None:
    result = operation.sweep()

    assert isinstance(result, list)
    assert all(isinstance(element, BoundSweepEvent) for element in result)
