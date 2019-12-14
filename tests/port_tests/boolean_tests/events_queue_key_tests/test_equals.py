from hypothesis import given

from martinez.boolean import EventsQueueKey
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.events_queue_keys)
def test_reflexivity(events_queue_key: EventsQueueKey) -> None:
    assert events_queue_key == events_queue_key


@given(strategies.events_queue_keys, strategies.events_queue_keys)
def test_symmetry(first_events_queue_key: EventsQueueKey,
                  second_events_queue_key: EventsQueueKey) -> None:
    assert equivalence(first_events_queue_key == second_events_queue_key,
                       second_events_queue_key == first_events_queue_key)


@given(strategies.events_queue_keys, strategies.events_queue_keys,
       strategies.events_queue_keys)
def test_transitivity(first_events_queue_key: EventsQueueKey,
                      second_events_queue_key: EventsQueueKey,
                      third_events_queue_key: EventsQueueKey) -> None:
    assert implication(first_events_queue_key == second_events_queue_key
                       and second_events_queue_key == third_events_queue_key,
                       first_events_queue_key == third_events_queue_key)


@given(strategies.events_queue_keys, strategies.events_queue_keys)
def test_connection_with_inequality(first_events_queue_key: EventsQueueKey,
                                    second_events_queue_key: EventsQueueKey
                                    ) -> None:
    assert equivalence(not first_events_queue_key == second_events_queue_key,
                       first_events_queue_key != second_events_queue_key)
