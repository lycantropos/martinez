from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.operations)
def test_round_trip(operation: BoundOperation) -> None:
    assert pickle_round_trip(operation) == operation
