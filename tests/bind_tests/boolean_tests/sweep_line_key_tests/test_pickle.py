from _martinez import SweepLineKey
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sweep_line_keys)
def test_round_trip(sweep_line_key: SweepLineKey) -> None:
    assert pickle_round_trip(sweep_line_key) == sweep_line_key
