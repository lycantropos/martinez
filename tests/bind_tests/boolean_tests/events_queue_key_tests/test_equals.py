from hypothesis import given

from tests.bind_tests.hints import BoundEventsQueueKey
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.events_queue_keys)
def test_reflexivity(key: BoundEventsQueueKey) -> None:
    assert key == key


@given(strategies.events_queue_keys, strategies.events_queue_keys)
def test_symmetry(first_key: BoundEventsQueueKey,
                  second_key: BoundEventsQueueKey) -> None:
    assert equivalence(first_key == second_key, second_key == first_key)


@given(strategies.events_queue_keys, strategies.events_queue_keys,
       strategies.events_queue_keys)
def test_transitivity(first_key: BoundEventsQueueKey,
                      second_key: BoundEventsQueueKey,
                      third_key: BoundEventsQueueKey) -> None:
    assert implication(first_key == second_key and second_key == third_key,
                       first_key == third_key)


@given(strategies.events_queue_keys, strategies.events_queue_keys)
def test_connection_with_inequality(first_key: BoundEventsQueueKey,
                                    second_key: BoundEventsQueueKey) -> None:
    assert equivalence(not first_key == second_key, first_key != second_key)
