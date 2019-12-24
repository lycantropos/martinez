from functools import partial
from itertools import repeat

from hypothesis import strategies

from tests.strategies import (booleans,
                              bound_with_ported_edges_types_pairs,
                              bound_with_ported_polygons_types_pairs,
                              make_cyclic_bound_with_ported_sweep_events,
                              single_precision_floats as floats,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_sweep_events,
                              unsigned_integers)

booleans = booleans
unsigned_integers = unsigned_integers
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
to_bound_with_ported_sweep_events = partial(
        to_bound_with_ported_sweep_events,
        booleans,
        bound_with_ported_points_pairs,
        polygons_types_pairs=bound_with_ported_polygons_types_pairs,
        edges_types_pairs=bound_with_ported_edges_types_pairs,
        in_outs=booleans,
        other_in_outs=booleans,
        in_results=booleans,
        positions=unsigned_integers)
nones_pairs = strategies.tuples(*repeat(strategies.none(), 2))
leaf_sweep_events_pairs = to_bound_with_ported_sweep_events(
        nones_pairs)
bound_with_ported_acyclic_sweep_events_pairs = strategies.recursive(
        leaf_sweep_events_pairs,
        to_bound_with_ported_sweep_events)
bound_with_ported_sweep_events_pairs = strategies.recursive(
        bound_with_ported_acyclic_sweep_events_pairs,
        make_cyclic_bound_with_ported_sweep_events)
bound_with_ported_nested_sweep_events_pairs = (
    to_bound_with_ported_sweep_events(bound_with_ported_sweep_events_pairs))
bound_with_ported_maybe_sweep_events_pairs = (
        nones_pairs | bound_with_ported_sweep_events_pairs)
