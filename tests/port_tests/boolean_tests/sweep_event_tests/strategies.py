from functools import partial

from hypothesis import strategies

from tests.strategies import (booleans,
                              non_negative_integers,
                              ported_edges_types,
                              ported_polygons_types,
                              scalars_strategies,
                              scalars_to_acyclic_ported_sweep_events,
                              scalars_to_nested_ported_sweep_events,
                              scalars_to_plain_ported_sweep_events,
                              scalars_to_ported_points,
                              scalars_to_ported_sweep_events)

booleans = booleans
non_negative_integers = non_negative_integers
polygons_types = ported_polygons_types
edges_types = ported_edges_types
points = scalars_strategies.flatmap(scalars_to_ported_points)
leaf_sweep_events = (scalars_strategies
                     .flatmap(partial(scalars_to_plain_ported_sweep_events,
                                      other_events=strategies.none())))
acyclic_sweep_events = (scalars_strategies
                        .flatmap(scalars_to_acyclic_ported_sweep_events))
sweep_events = scalars_strategies.flatmap(scalars_to_ported_sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
maybe_sweep_events = strategies.none() | sweep_events
