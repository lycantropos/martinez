import pickle

from _martinez import EventsQueueKey
from hypothesis import given

from . import strategies


@given(strategies.events_queue_keys)
def test_round_trip(events_queue_key: EventsQueueKey) -> None:
    assert pickle.loads(pickle.dumps(events_queue_key)) == events_queue_key
