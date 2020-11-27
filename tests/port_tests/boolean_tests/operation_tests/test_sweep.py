from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.pre_processed_non_trivial_operations)
def test_basic(operation: PortedOperation) -> None:
    result = operation.sweep()

    assert isinstance(result, list)
    assert all(isinstance(element, PortedSweepEvent) for element in result)
