from hypothesis import given

from tests.port_tests.hints import PortedOperation
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.operations)
def test_round_trip(operation: PortedOperation) -> None:
    assert pickle_round_trip(operation) == operation
