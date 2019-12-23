from hypothesis import strategies

from martinez.boolean import SweepLineKey
from tests.strategies import (scalars_strategies,
                              scalars_to_nested_ported_sweep_events,
                              scalars_to_ported_sweep_events)

sweep_events = scalars_strategies.flatmap(scalars_to_ported_sweep_events)
sweep_line_keys = strategies.builds(SweepLineKey, sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
nested_sweep_line_keys = strategies.builds(SweepLineKey, nested_sweep_events)
non_sweep_line_keys = strategies.builds(object)
