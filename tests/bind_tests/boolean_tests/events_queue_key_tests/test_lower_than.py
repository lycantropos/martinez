from typing import (Any,
                    Tuple)

import pytest
from _martinez import EventsQueueKey
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.nested_events_queue_keys)
def test_irreflexivity(events_queue_key: EventsQueueKey) -> None:
    assert not events_queue_key < events_queue_key


@given(strategies.nested_events_queue_keys,
       strategies.nested_events_queue_keys)
def test_asymmetry(first_key: EventsQueueKey,
                   second_key: EventsQueueKey) -> None:
    assert implication(first_key < second_key, not second_key < first_key)


@given(strategies.totally_ordered_nested_events_queue_keys_triplets)
def test_transitivity(keys_triplet: Tuple[EventsQueueKey,
                                          EventsQueueKey,
                                          EventsQueueKey]) -> None:
    first_key, second_key, third_key = keys_triplet

    assert implication(first_key < second_key < third_key,
                       first_key < third_key)


@given(strategies.nested_events_queue_keys,
       strategies.nested_events_queue_keys)
def test_connection_with_greater_than(first_key: EventsQueueKey,
                                      second_key: EventsQueueKey) -> None:
    assert equivalence(first_key < second_key, second_key > first_key)


@given(strategies.nested_events_queue_keys, strategies.non_events_queue_keys)
def test_non_key(key: EventsQueueKey, non_key: Any) -> None:
    with pytest.raises(TypeError):
        key < non_key