from hypothesis import strategies

from tests.port_tests.factories import (scalars_to_nested_ported_sweep_events,
                                        scalars_to_ported_sweep_events)
from tests.port_tests.hints import PortedSweepLineKey
from tests.strategies import scalars_strategies
from tests.utils import (identity,
                         to_builder,
                         to_pairs,
                         to_triplets)

sweep_events_strategies = (scalars_strategies
                           .map(scalars_to_ported_sweep_events))
sweep_events = sweep_events_strategies.flatmap(identity)
sweep_line_keys_strategies = (sweep_events_strategies
                              .map(to_builder(PortedSweepLineKey)))
sweep_line_keys = sweep_line_keys_strategies.flatmap(identity)
sweep_line_keys_pairs = sweep_line_keys_strategies.flatmap(to_pairs)
sweep_line_keys_triplets = sweep_line_keys_strategies.flatmap(to_triplets)
nested_sweep_events_strategies = (scalars_strategies
                                  .map(scalars_to_nested_ported_sweep_events))
nested_sweep_line_keys_strategies = (nested_sweep_events_strategies
                                     .map(to_builder(PortedSweepLineKey)))
nested_sweep_line_keys = nested_sweep_line_keys_strategies.flatmap(identity)
nested_sweep_line_keys_pairs = (nested_sweep_line_keys_strategies
                                .flatmap(to_pairs))
non_sweep_line_keys = strategies.builds(object)
