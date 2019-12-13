from functools import partial
from itertools import repeat

from _martinez import (EdgeType as BoundEdgeType,
                       PolygonType as BoundPolygonType)
from hypothesis import strategies

from martinez.boolean import (EdgeType as PortedEdgeType,
                              PolygonType as PortedPolygonType)
from tests.strategies import (booleans,
                              make_cyclic_bound_with_ported_sweep_events,
                              single_precision_floats as floats,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_sweep_events)

booleans = booleans
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_polygons_types_pairs = strategies.sampled_from(
        [(BoundPolygonType.__members__[name],
          PortedPolygonType.__members__[name])
         for name in (BoundPolygonType.__members__.keys() &
                      PortedPolygonType.__members__.keys())])
bound_with_ported_edges_types_pairs = strategies.sampled_from(
        [(BoundEdgeType.__members__[name],
          PortedEdgeType.__members__[name])
         for name in (BoundEdgeType.__members__.keys() &
                      PortedEdgeType.__members__.keys())])
to_bound_with_ported_sweep_events = partial(
        to_bound_with_ported_sweep_events,
        booleans,
        bound_with_ported_points_pairs,
        polygons_types_pairs=bound_with_ported_polygons_types_pairs,
        edges_types_pairs=bound_with_ported_edges_types_pairs)
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
