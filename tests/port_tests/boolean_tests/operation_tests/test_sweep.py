from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from . import strategies


@given(strategies.pre_processed_non_trivial_operations)
def test_basic(operation: Operation) -> None:
    result = operation.sweep()

    assert isinstance(result, list)
    assert all(isinstance(element, SweepEvent) for element in result)
