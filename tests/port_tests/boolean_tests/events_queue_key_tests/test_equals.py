from typing import Tuple

from hypothesis import given

from tests.port_tests.hints import PortedEventsQueueKey
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.events_queue_keys)
def test_reflexivity(key: PortedEventsQueueKey) -> None:
    assert key == key


@given(strategies.events_queue_keys_pairs)
def test_symmetry(keys_pair: Tuple[PortedEventsQueueKey, PortedEventsQueueKey]
                  ) -> None:
    first_key, second_key = keys_pair

    assert equivalence(first_key == second_key, second_key == first_key)


@given(strategies.events_queue_keys_triplets)
def test_transitivity(keys_pair: Tuple[PortedEventsQueueKey,
                                       PortedEventsQueueKey,
                                       PortedEventsQueueKey]) -> None:
    first_key, second_key, third_key = keys_pair

    assert implication(first_key == second_key and second_key == third_key,
                       first_key == third_key)


@given(strategies.events_queue_keys_pairs)
def test_connection_with_inequality(keys_pair: Tuple[PortedEventsQueueKey,
                                                     PortedEventsQueueKey]
                                    ) -> None:
    first_key, second_key = keys_pair

    assert equivalence(not first_key == second_key, first_key != second_key)
