import pickle

from _martinez import SweepEvent
from hypothesis import given

from . import strategies


@given(strategies.sweep_events)
def test_round_trip(sweep_event: SweepEvent) -> None:
    assert pickle.loads(pickle.dumps(sweep_event)) == sweep_event
