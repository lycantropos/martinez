from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sweep_events)
def test_round_trip(event: BoundSweepEvent) -> None:
    assert pickle_round_trip(event) == event
