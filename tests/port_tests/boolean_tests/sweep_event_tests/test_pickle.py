from hypothesis import given

from martinez.boolean import SweepEvent
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sweep_events)
def test_round_trip(event: SweepEvent) -> None:
    assert pickle_round_trip(event) == event
