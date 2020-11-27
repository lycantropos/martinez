from hypothesis import strategies

from tests.strategies import (booleans,
                              bound_with_ported_edges_types_pairs,
                              bound_with_ported_polygons_types_pairs,
                              single_precision_floats as floats,
                              unsigned_integers)
from tests.integration_tests.factories import \
    make_cyclic_bound_with_ported_sweep_events, \
    to_bound_with_ported_points_pair, \
    to_bound_with_ported_sweep_events
from tests.utils import (MAX_NESTING_DEPTH,
                         to_pairs)

booleans = booleans
polygons_types_pairs = bound_with_ported_polygons_types_pairs
edges_types_pairs = bound_with_ported_edges_types_pairs
unsigned_integers = unsigned_integers
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
nones_pairs = to_pairs(strategies.none())
leaf_sweep_events_pairs = to_bound_with_ported_sweep_events(nones_pairs)
acyclic_sweep_events_pairs = strategies.recursive(
        leaf_sweep_events_pairs, to_bound_with_ported_sweep_events,
        max_leaves=MAX_NESTING_DEPTH)
sweep_events_pairs = make_cyclic_bound_with_ported_sweep_events(
        acyclic_sweep_events_pairs)
nested_sweep_events_pairs = to_bound_with_ported_sweep_events(
        sweep_events_pairs)
maybe_sweep_events_pairs = nones_pairs | sweep_events_pairs
