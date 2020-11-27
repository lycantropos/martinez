from typing import (Any,
                    Tuple)

import pytest
from hypothesis import given

from tests.bind_tests.hints import BoundEventsQueueKey
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.nested_events_queue_keys)
def test_irreflexivity(key: BoundEventsQueueKey) -> None:
    assert not key < key


@given(strategies.nested_events_queue_keys,
       strategies.nested_events_queue_keys)
def test_asymmetry(first_key: BoundEventsQueueKey,
                   second_key: BoundEventsQueueKey) -> None:
    assert implication(first_key < second_key, not second_key < first_key)


@given(strategies.totally_ordered_nested_events_queue_keys_triplets)
def test_transitivity(keys_triplet: Tuple[BoundEventsQueueKey,
                                          BoundEventsQueueKey,
                                          BoundEventsQueueKey]) -> None:
    first_key, second_key, third_key = keys_triplet

    assert implication(first_key < second_key < third_key,
                       first_key < third_key)


@given(strategies.nested_events_queue_keys,
       strategies.nested_events_queue_keys)
def test_connection_with_greater_than(first_key: BoundEventsQueueKey,
                                      second_key: BoundEventsQueueKey) -> None:
    assert equivalence(first_key < second_key, second_key > first_key)


@given(strategies.nested_events_queue_keys, strategies.non_events_queue_keys)
def test_non_key(key: BoundEventsQueueKey, non_key: Any) -> None:
    with pytest.raises(TypeError):
        key < non_key
