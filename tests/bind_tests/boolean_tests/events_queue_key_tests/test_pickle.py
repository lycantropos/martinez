from _martinez import EventsQueueKey
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.events_queue_keys)
def test_round_trip(key: EventsQueueKey) -> None:
    assert pickle_round_trip(key) == key
