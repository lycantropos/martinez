from itertools import repeat
from typing import (List,
                    Tuple)

from _martinez import (Operation as Bound,
                       OperationType as BoundOperationType,
                       Point as BoundPoint,
                       Polygon as BoundPolygon,
                       SweepEvent as BoundSweepEvent)
from hypothesis import strategies

from martinez.boolean import (Operation as Ported,
                              OperationType as PortedOperationType,
                              SweepEvent as PortedSweepEvent)
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from tests.strategies import (booleans,
                              bound_with_ported_operations_types_pairs,
                              make_cyclic_bound_with_ported_sweep_events,
                              single_precision_floats as floats,
                              to_bound_with_ported_contours_pair,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_polygons_pair,
                              to_bound_with_ported_sweep_events,
                              unsigned_integers_lists)
from tests.utils import (are_non_overlapping_sweep_events_pair,
                         are_sweep_events_pair_with_different_polygon_types,
                         transpose,
                         vertices_form_strict_polygon)

booleans = booleans
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
nones_pairs = strategies.tuples(*repeat(strategies.none(), 2))
leaf_sweep_events_pairs = to_bound_with_ported_sweep_events(nones_pairs)
acyclic_sweep_events_pairs = strategies.recursive(
        leaf_sweep_events_pairs, to_bound_with_ported_sweep_events)
sweep_events_pairs = strategies.recursive(
        acyclic_sweep_events_pairs, make_cyclic_bound_with_ported_sweep_events)
nested_sweep_events_pairs = to_bound_with_ported_sweep_events(
        sweep_events_pairs)
nested_sweep_events_pairs_pairs = (
    strategies.tuples(*repeat(nested_sweep_events_pairs, 2)).map(transpose))


def are_non_overlapping_sweep_events_pair_pair(
        events_pair_pair: Tuple[Tuple[BoundSweepEvent, BoundSweepEvent],
                                Tuple[PortedSweepEvent, PortedSweepEvent]]
) -> bool:
    bound_events_pair, ported_events_pair = events_pair_pair
    return (are_non_overlapping_sweep_events_pair(bound_events_pair)
            and are_non_overlapping_sweep_events_pair(ported_events_pair))


def are_sweep_events_pair_pair_with_different_polygon_types(
        events_pair_pair: Tuple[Tuple[BoundSweepEvent, BoundSweepEvent],
                                Tuple[PortedSweepEvent, PortedSweepEvent]]
) -> bool:
    bound_events_pair, ported_events_pair = events_pair_pair
    return (are_sweep_events_pair_with_different_polygon_types(
            bound_events_pair)
            and are_sweep_events_pair_with_different_polygon_types(
                    ported_events_pair))


nested_sweep_events_pairs_pairs = (
        nested_sweep_events_pairs_pairs
        .filter(are_non_overlapping_sweep_events_pair_pair)
        | nested_sweep_events_pairs_pairs
        .filter(are_sweep_events_pair_pair_with_different_polygon_types))
operations_types_pairs = bound_with_ported_operations_types_pairs


def vertices_pair_form_strict_polygons(vertices_pair: Tuple[List[BoundPoint],
                                                            List[PortedPoint]]
                                       ) -> bool:
    bound_vertices, ported_vertices = vertices_pair
    return (vertices_form_strict_polygon(bound_vertices)
            and vertices_form_strict_polygon(ported_vertices))


vertices_pairs = (strategies.lists(points_pairs,
                                   min_size=3,
                                   max_size=3)
                  .map(transpose)
                  .filter(vertices_pair_form_strict_polygons))
contours_pairs = strategies.builds(to_bound_with_ported_contours_pair,
                                   vertices_pairs, unsigned_integers_lists,
                                   booleans)
contours_lists_pairs = strategies.lists(contours_pairs).map(transpose)
empty_contours_lists_pairs = strategies.tuples(*repeat(strategies.builds(list),
                                                       2))
non_empty_contours_lists_pairs = strategies.lists(contours_pairs,
                                                  min_size=1).map(transpose)
polygons_pairs = strategies.builds(to_bound_with_ported_polygons_pair,
                                   contours_lists_pairs)
empty_polygons_pairs = strategies.builds(to_bound_with_ported_polygons_pair,
                                         empty_contours_lists_pairs)
non_empty_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        non_empty_contours_lists_pairs)


def to_bound_with_ported_operations_pair(
        left_polygons_pair: Tuple[BoundPolygon, PortedPolygon],
        right_polygons_pair: Tuple[BoundPolygon, PortedPolygon],
        operations_types_pair: Tuple[BoundOperationType, PortedOperationType],
) -> Tuple[Bound, Ported]:
    bound_left, ported_left = left_polygons_pair
    bound_right, ported_right = right_polygons_pair
    (bound_operation_type,
     ported_operation_type) = operations_types_pair
    return (Bound(bound_left, bound_right, bound_operation_type),
            Ported(ported_left, ported_right, ported_operation_type))


operations_pairs = strategies.builds(to_bound_with_ported_operations_pair,
                                     polygons_pairs, polygons_pairs,
                                     operations_types_pairs)
