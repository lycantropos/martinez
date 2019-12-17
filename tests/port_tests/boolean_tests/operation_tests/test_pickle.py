from hypothesis import given

from martinez.boolean import Operation
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.operations)
def test_round_trip(operation: Operation) -> None:
    assert pickle_round_trip(operation) == operation
