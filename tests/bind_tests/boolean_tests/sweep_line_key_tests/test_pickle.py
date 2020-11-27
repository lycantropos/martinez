from hypothesis import given

from tests.bind_tests.hints import BoundSweepLineKey
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sweep_line_keys)
def test_round_trip(key: BoundSweepLineKey) -> None:
    assert pickle_round_trip(key) == key
