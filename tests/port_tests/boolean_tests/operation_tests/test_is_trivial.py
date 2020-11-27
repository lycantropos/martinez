from hypothesis import given

from tests.port_tests.hints import PortedOperation
from . import strategies


@given(strategies.operations)
def test_basic(operation: PortedOperation) -> None:
    assert isinstance(operation.is_trivial, bool)
