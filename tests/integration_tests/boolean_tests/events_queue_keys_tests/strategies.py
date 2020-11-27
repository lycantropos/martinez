from typing import Tuple

from _martinez import (EventsQueueKey as BoundEventsQueueKey,
                       SweepEvent as BoundSweepEvent)
from hypothesis import strategies

from martinez.boolean import (EventsQueueKey as PortedEventsQueueKey,
                              SweepEvent as PortedSweepEvent)
from tests.integration_tests.factories import (
    make_cyclic_bound_with_ported_sweep_events,
    to_bound_with_ported_sweep_events)
from tests.strategies import booleans
from tests.utils import (MAX_NESTING_DEPTH,
                         to_pairs)

booleans = booleans
nones_pairs = to_pairs(strategies.none())
leaf_sweep_events_pairs = to_bound_with_ported_sweep_events(nones_pairs)
acyclic_sweep_events_pairs = strategies.recursive(
        leaf_sweep_events_pairs, to_bound_with_ported_sweep_events,
        max_leaves=MAX_NESTING_DEPTH)
sweep_events_pairs = make_cyclic_bound_with_ported_sweep_events(
        acyclic_sweep_events_pairs)


def to_events_queue_keys_pair(sweep_events_pair: Tuple[BoundSweepEvent,
                                                       PortedSweepEvent]
                              ) -> Tuple[BoundEventsQueueKey,
                                         PortedEventsQueueKey]:
    bound_event, ported_event = sweep_events_pair
    return BoundEventsQueueKey(bound_event), PortedEventsQueueKey(ported_event)


events_queue_keys_pairs = strategies.builds(to_events_queue_keys_pair,
                                            sweep_events_pairs)
nested_sweep_events_pairs = to_bound_with_ported_sweep_events(
        sweep_events_pairs)
nested_events_queue_keys_pairs = strategies.builds(to_events_queue_keys_pair,
                                                   nested_sweep_events_pairs)
