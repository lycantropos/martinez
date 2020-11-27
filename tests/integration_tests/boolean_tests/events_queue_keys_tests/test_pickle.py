from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundEventsQueueKey
from tests.integration_tests.utils import (
    are_bound_ported_events_queue_keys_equal)
from tests.port_tests.hints import PortedEventsQueueKey
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.events_queue_keys_pairs)
def test_round_trip(events_queue_keys_pair
                    : Tuple[BoundEventsQueueKey, PortedEventsQueueKey]
                    ) -> None:
    bound, ported = events_queue_keys_pair

    assert are_bound_ported_events_queue_keys_equal(pickle_round_trip(bound),
                                                    pickle_round_trip(ported))
