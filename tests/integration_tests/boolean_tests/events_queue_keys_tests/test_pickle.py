import pickle
from typing import Tuple

from _martinez import EventsQueueKey as Bound
from hypothesis import given

from martinez.boolean import EventsQueueKey as Ported
from tests.utils import are_bound_ported_events_queue_keys_equal
from . import strategies


@given(strategies.bound_with_ported_events_queue_keys_pairs)
def test_round_trip(
        bound_with_ported_events_queue_keys_pair: Tuple[Bound, Ported]
) -> None:
    bound, ported = bound_with_ported_events_queue_keys_pair

    assert are_bound_ported_events_queue_keys_equal(
            pickle.loads(pickle.dumps(bound)),
            pickle.loads(pickle.dumps(ported)))
