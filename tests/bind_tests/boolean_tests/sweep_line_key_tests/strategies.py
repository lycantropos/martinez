from hypothesis import strategies

from tests.bind_tests.factories import (to_bound_sweep_events,
                                        to_nested_bound_sweep_events)
from tests.bind_tests.hints import BoundSweepLineKey

sweep_events = to_bound_sweep_events()
sweep_line_keys = strategies.builds(BoundSweepLineKey, sweep_events)
nested_sweep_events = to_nested_bound_sweep_events()
nested_sweep_line_keys = strategies.builds(BoundSweepLineKey,
                                           nested_sweep_events)
non_sweep_line_keys = strategies.builds(object)
