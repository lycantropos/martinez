from hypothesis import given

from tests.bind_tests.hints import BoundEventsQueueKey
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.events_queue_keys)
def test_round_trip(key: BoundEventsQueueKey) -> None:
    assert pickle_round_trip(key) == key
