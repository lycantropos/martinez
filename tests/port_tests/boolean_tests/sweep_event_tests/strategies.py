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
from tests.utils import (cleave_in_tuples,
                         identity,
                         to_maybe,
                         to_pairs,
                         to_triplets)

booleans = booleans
non_negative_integers = non_negative_integers
polygons_types = ported_polygons_types
edges_types = ported_edges_types
points = scalars_strategies.flatmap(scalars_to_ported_points)
leaf_sweep_events = (scalars_strategies
                     .flatmap(partial(scalars_to_plain_ported_sweep_events,
                                      children=strategies.none())))
leaf_sweep_events_with_points = scalars_strategies.flatmap(
        cleave_in_tuples(partial(scalars_to_plain_ported_sweep_events,
                                 children=strategies.none()),
                         scalars_to_ported_points))
acyclic_sweep_events = (scalars_strategies
                        .flatmap(scalars_to_acyclic_ported_sweep_events))
sweep_events_strategies = (scalars_strategies
                           .map(scalars_to_ported_sweep_events))
sweep_events = sweep_events_strategies.flatmap(identity)
sweep_events_pairs = sweep_events_strategies.flatmap(to_pairs)
sweep_events_triplets = sweep_events_strategies.flatmap(to_triplets)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
nested_sweep_events_with_points = scalars_strategies.flatmap(
        cleave_in_tuples(scalars_to_nested_ported_sweep_events,
                         scalars_to_ported_points))
maybe_sweep_events = to_maybe(sweep_events)
