from functools import partial

from hypothesis import strategies

from martinez.boolean import SweepLineKey
from tests.strategies import (booleans,
                              make_cyclic,
                              ported_edges_types,
                              ported_polygons_types,
                              scalars_strategies,
                              scalars_to_ported_points,
                              scalars_to_ported_sweep_events,
                              to_ported_sweep_events)

booleans = booleans
polygons_types = ported_polygons_types
edges_types = ported_edges_types
points = scalars_strategies.flatmap(scalars_to_ported_points)
leaf_sweep_events = (scalars_strategies
                     .flatmap(partial(to_ported_sweep_events,
                                      other_events=strategies.none())))
acyclic_sweep_events = (scalars_strategies
                        .flatmap(scalars_to_ported_sweep_events))
sweep_events = strategies.recursive(acyclic_sweep_events, make_cyclic)
sweep_line_keys = strategies.builds(SweepLineKey, sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(partial(to_ported_sweep_events,
                                        other_events=sweep_events)))
nested_sweep_line_keys = strategies.builds(SweepLineKey,
                                           nested_sweep_events)
non_sweep_line_keys = strategies.builds(object)
