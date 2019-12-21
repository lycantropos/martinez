from functools import partial
from itertools import repeat
from typing import (List,
                    Tuple)

from _martinez import (Operation as Bound,
                       OperationType as BoundOperationType,
                       Point as BoundPoint,
                       Polygon as BoundPolygon)
from hypothesis import strategies

from martinez.boolean import (Operation as Ported,
                              OperationType as PortedOperationType)
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from tests.strategies import (booleans,
                              bound_with_ported_edges_types_pairs,
                              bound_with_ported_operations_types_pairs,
                              bound_with_ported_polygons_types_pairs,
                              make_cyclic_bound_with_ported_sweep_events,
                              single_precision_floats as floats,
                              to_bound_with_ported_contours_pair,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_polygons_pair,
                              to_bound_with_ported_sweep_events,
                              unsigned_integers_lists)
from tests.utils import (transpose,
                         vertices_form_strict_polygon)

booleans = booleans
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
nones_pairs = strategies.tuples(*repeat(strategies.none(), 2))
to_bound_with_ported_sweep_events = partial(
        to_bound_with_ported_sweep_events,
        booleans,
        bound_with_ported_points_pairs,
        polygons_types_pairs=bound_with_ported_polygons_types_pairs,
        edges_types_pairs=bound_with_ported_edges_types_pairs)
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
bound_with_ported_operations_types_pairs = (
    bound_with_ported_operations_types_pairs)
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)


def bound_with_ported_vertices_form_strict_polygon(
        bound_with_ported_vertices_pair: Tuple[List[BoundPoint],
                                               List[PortedPoint]]
) -> bool:
    bound_vertices, ported_vertices = bound_with_ported_vertices_pair
    return (vertices_form_strict_polygon(bound_vertices)
            and vertices_form_strict_polygon(ported_vertices))


bound_with_ported_vertices_pairs = (
    (strategies.lists(bound_with_ported_points_pairs,
                      min_size=3,
                      max_size=3)
     .map(transpose)
     .filter(bound_with_ported_vertices_form_strict_polygon)))
bound_with_ported_contours_pairs = strategies.builds(
        to_bound_with_ported_contours_pair,
        bound_with_ported_vertices_pairs,
        unsigned_integers_lists,
        booleans)
bound_with_ported_contours_lists_pairs = strategies.lists(
        bound_with_ported_contours_pairs).map(transpose)
bound_with_ported_empty_contours_lists_pairs = strategies.tuples(
        *repeat(strategies.builds(list), 2))
bound_with_ported_non_empty_contours_lists_pairs = strategies.lists(
        bound_with_ported_contours_pairs,
        min_size=1).map(transpose)
bound_with_ported_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        bound_with_ported_contours_lists_pairs)
bound_with_ported_empty_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        bound_with_ported_empty_contours_lists_pairs)
bound_with_ported_non_empty_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        bound_with_ported_non_empty_contours_lists_pairs)


def to_bound_with_ported_operations_pair(
        bound_with_ported_left_polygons_pair: Tuple[BoundPolygon,
                                                    PortedPolygon],
        bound_with_ported_right_polygons_pair: Tuple[BoundPolygon,
                                                     PortedPolygon],
        bound_with_ported_operations_types_pair: Tuple[BoundOperationType,
                                                       PortedOperationType],
) -> Tuple[Bound, Ported]:
    bound_left, ported_left = bound_with_ported_left_polygons_pair
    bound_right, ported_right = bound_with_ported_right_polygons_pair
    (bound_operation_type,
     ported_operation_type) = bound_with_ported_operations_types_pair
    return (Bound(bound_left, bound_right, bound_operation_type),
            Ported(ported_left, ported_right, ported_operation_type))


bound_with_ported_operations_pairs = strategies.builds(
        to_bound_with_ported_operations_pair,
        bound_with_ported_polygons_pairs, bound_with_ported_polygons_pairs,
        bound_with_ported_operations_types_pairs)
