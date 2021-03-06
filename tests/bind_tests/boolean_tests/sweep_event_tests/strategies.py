from hypothesis import strategies

from tests.bind_tests.factories import (to_acyclic_bound_sweep_events,
                                        to_bound_sweep_events,
                                        to_nested_bound_sweep_events,
                                        to_plain_bound_sweep_events)
from tests.bind_tests.hints import BoundPoint
from tests.bind_tests.utils import (bound_edges_types,
                                    bound_polygons_types)
from tests.strategies import (booleans,
                              floats,
                              unsigned_integers)

booleans = booleans
unsigned_integers = unsigned_integers
points = strategies.builds(BoundPoint, floats, floats)
polygons_types = bound_polygons_types
edges_types = bound_edges_types
leaf_sweep_events = to_plain_bound_sweep_events(strategies.none())
acyclic_sweep_events = to_acyclic_bound_sweep_events()
sweep_events = to_bound_sweep_events()
nested_sweep_events = to_nested_bound_sweep_events()
maybe_sweep_events = strategies.none() | sweep_events
