from hypothesis import strategies

from martinez.boolean import EventsQueueKey
from tests.strategies import (scalars_strategies,
                              scalars_to_nested_ported_sweep_events,
                              scalars_to_ported_sweep_events)

sweep_events = scalars_strategies.flatmap(scalars_to_ported_sweep_events)
events_queue_keys = strategies.builds(EventsQueueKey, sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
nested_events_queue_keys = strategies.builds(EventsQueueKey,
                                             nested_sweep_events)
non_events_queue_keys = strategies.builds(object)
