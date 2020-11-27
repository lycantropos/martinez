from _martinez import SweepLineKey
from hypothesis import strategies

from tests.bind_tests.factories import to_bound_sweep_events, \
    to_nested_bound_sweep_events

sweep_events = to_bound_sweep_events()
sweep_line_keys = strategies.builds(SweepLineKey, sweep_events)
nested_sweep_events = to_nested_bound_sweep_events()
nested_sweep_line_keys = strategies.builds(SweepLineKey,
                                           nested_sweep_events)
non_sweep_line_keys = strategies.builds(object)
