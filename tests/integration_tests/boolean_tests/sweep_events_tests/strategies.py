from itertools import repeat
from typing import (Optional,
                    Tuple)

from _martinez import (EdgeType as BoundEdgeType,
                       Point as BoundPoint,
                       PolygonType as BoundPolygonType,
                       SweepEvent as Bound)
from hypothesis import strategies

from martinez.boolean import (EdgeType as PortedEdgeType,
                              PolygonType as PortedPolygonType,
                              SweepEvent as Ported)
from martinez.point import Point as PortedPoint
from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_points_pair,
                              to_cyclic_sweep_event)
from tests.utils import Strategy

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


def to_bound_with_ported_sweep_events(
        bound_with_ported_children: Strategy[Tuple[Optional[Bound],
                                                   Optional[Ported]]]
) -> Strategy[Tuple[Bound, Ported]]:
    def to_sweep_events(
            is_left: bool,
            bound_with_ported_points_pair: Tuple[BoundPoint, PortedPoint],
            bound_with_ported_other_events_pair: Tuple[Bound, Ported],
            bound_with_ported_polygons_types_pair: Tuple[BoundPolygonType,
                                                         PortedPolygonType],
            bound_with_ported_edges_types_pair: Tuple[BoundEdgeType,
                                                      PortedEdgeType]
    ) -> Tuple[Bound, Ported]:
        bound_point, ported_point = bound_with_ported_points_pair
        (bound_other_event,
         ported_other_event) = bound_with_ported_other_events_pair
        (bound_polygon_type,
         ported_polygon_type) = bound_with_ported_polygons_types_pair
        bound_edge_type, ported_edge_type = bound_with_ported_edges_types_pair
        bound = Bound(is_left, bound_point, bound_other_event,
                      bound_polygon_type,
                      bound_edge_type)
        ported = Ported(is_left, ported_point, ported_other_event,
                        ported_polygon_type, ported_edge_type)
        return bound, ported

    return strategies.builds(to_sweep_events,
                             booleans, bound_with_ported_points_pairs,
                             bound_with_ported_children,
                             bound_with_ported_polygons_types_pairs,
                             bound_with_ported_edges_types_pairs)


nones_pairs = strategies.tuples(*repeat(strategies.none(), 2))
bound_with_ported_leaf_sweep_events_pairs = to_bound_with_ported_sweep_events(
        nones_pairs)
bound_with_ported_acyclic_sweep_events_pairs = strategies.recursive(
        bound_with_ported_leaf_sweep_events_pairs,
        to_bound_with_ported_sweep_events)


def make_cyclic(sweep_events_pairs: Strategy[Tuple[Bound, Ported]]
                ) -> Strategy[Tuple[Bound, Ported]]:
    def to_cyclic_sweep_events(sweep_events_pair: Tuple[Bound, Ported],
                               source_index_seed: int,
                               destination_index_seed: int
                               ) -> Tuple[Bound, Ported]:
        bound, ported = sweep_events_pair
        return (to_cyclic_sweep_event(bound, source_index_seed,
                                      destination_index_seed),
                to_cyclic_sweep_event(ported, source_index_seed,
                                      destination_index_seed))

    return strategies.builds(to_cyclic_sweep_events,
                             sweep_events_pairs,
                             strategies.integers(),
                             strategies.integers())


bound_with_ported_sweep_events_pairs = strategies.recursive(
        bound_with_ported_acyclic_sweep_events_pairs,
        make_cyclic)
bound_with_ported_nested_sweep_events_pairs = (
    to_bound_with_ported_sweep_events(bound_with_ported_sweep_events_pairs))
bound_with_ported_maybe_sweep_events_pairs = (
        nones_pairs | bound_with_ported_sweep_events_pairs)
