from hypothesis import given

from martinez.boolean import EventsQueueKey as PortedEventsQueueKey
from tests.bind_tests.hints import BoundEventsQueueKey
from tests.integration_tests.hints import BoundPortedSweepEventsPair
from tests.integration_tests.utils import (
    are_bound_ported_events_queue_keys_equal)
from . import strategies


@given(strategies.sweep_events_pairs)
def test_basic(events_pair: BoundPortedSweepEventsPair) -> None:
    bound_event, ported_event = events_pair

    bound = BoundEventsQueueKey(bound_event)
    ported = PortedEventsQueueKey(ported_event)

    assert are_bound_ported_events_queue_keys_equal(bound, ported)
