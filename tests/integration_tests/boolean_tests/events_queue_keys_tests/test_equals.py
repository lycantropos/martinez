from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundEventsQueueKey
from tests.port_tests.hints import PortedEventsQueueKey
from tests.utils import equivalence
from . import strategies


@given(strategies.events_queue_keys_pairs,
       strategies.events_queue_keys_pairs)
def test_basic(first_events_queue_keys_pair: Tuple[BoundEventsQueueKey,
                                                   PortedEventsQueueKey],
               second_events_queue_keys_pair: Tuple[BoundEventsQueueKey,
                                                    PortedEventsQueueKey]
               ) -> None:
    first_bound, first_ported = first_events_queue_keys_pair
    second_bound, second_ported = second_events_queue_keys_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
