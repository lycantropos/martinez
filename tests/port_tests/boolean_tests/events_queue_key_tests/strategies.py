from hypothesis import strategies

from martinez.boolean import EventsQueueKey
from tests.strategies import (scalars_strategies)
from tests.port_tests.factories import scalars_to_nested_ported_sweep_events, \
    scalars_to_ported_sweep_events
from tests.utils import (identity,
                         to_builder,
                         to_pairs,
                         to_triplets)

sweep_events_strategies = (scalars_strategies
                           .map(scalars_to_ported_sweep_events))
sweep_events = sweep_events_strategies.flatmap(identity)
events_queue_keys_strategies = (sweep_events_strategies
                                .map(to_builder(EventsQueueKey)))
events_queue_keys = events_queue_keys_strategies.flatmap(identity)
events_queue_keys_pairs = events_queue_keys_strategies.flatmap(to_pairs)
events_queue_keys_triplets = events_queue_keys_strategies.flatmap(to_triplets)
nested_sweep_events_strategies = (scalars_strategies
                                  .map(scalars_to_nested_ported_sweep_events))
nested_events_queue_keys_strategies = (nested_sweep_events_strategies
                                       .map(to_builder(EventsQueueKey)))
nested_events_queue_keys = (nested_events_queue_keys_strategies
                            .flatmap(identity))
nested_events_queue_keys_pairs = (nested_events_queue_keys_strategies
                                  .flatmap(to_pairs))
nested_events_queue_keys_triplets = (nested_events_queue_keys_strategies
                                     .flatmap(to_triplets))
non_events_queue_keys = strategies.builds(object)
