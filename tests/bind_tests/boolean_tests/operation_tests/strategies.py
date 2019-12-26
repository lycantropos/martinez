from typing import (List,
                    Tuple)

from _martinez import (Contour,
                       Operation,
                       OperationType,
                       Point,
                       Polygon,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              bound_operations_types,
                              floats,
                              to_bound_sweep_events,
                              to_nested_bound_sweep_events,
                              unsigned_integers_lists)
from tests.utils import (are_non_overlapping_sweep_events_pair,
                         are_sweep_events_pair_with_different_polygon_types,
                         is_sweep_event_non_degenerate,
                         vertices_form_strict_polygon)

points = strategies.builds(Point, floats, floats)
sweep_events = to_bound_sweep_events()
nested_sweep_events = to_nested_bound_sweep_events()
nested_sweep_events_lists = strategies.lists(nested_sweep_events)
non_degenerate_nested_sweep_events = (nested_sweep_events
                                      .filter(is_sweep_event_non_degenerate))
nested_sweep_events_pairs = strategies.tuples(nested_sweep_events,
                                              nested_sweep_events)
nested_sweep_events_pairs = (
        nested_sweep_events_pairs
        .filter(are_non_overlapping_sweep_events_pair)
        | nested_sweep_events_pairs
        .filter(are_sweep_events_pair_with_different_polygon_types))
operations_types = bound_operations_types
triangles_vertices = (strategies.lists(strategies.builds(Point,
                                                         floats, floats),
                                       min_size=3,
                                       max_size=3)
                      .filter(vertices_form_strict_polygon))
contours_vertices = triangles_vertices
contours = strategies.builds(Contour, contours_vertices,
                             unsigned_integers_lists, booleans)
contours_lists = strategies.lists(contours)
empty_contours_lists = strategies.builds(list)
non_empty_contours_lists = strategies.lists(contours,
                                            min_size=1,
                                            max_size=1)
polygons = strategies.builds(Polygon, contours_lists)
empty_polygons = strategies.builds(Polygon, empty_contours_lists)
non_empty_polygons = strategies.builds(Polygon, non_empty_contours_lists)


def to_non_overlapping_polygons_pair(first_polygon: Polygon,
                                     second_polygon: Polygon
                                     ) -> Tuple[Polygon, Polygon]:
    first_bounding_box = first_polygon.bounding_box
    second_bounding_box = second_polygon.bounding_box
    delta_x = (max(first_bounding_box.x_max, second_bounding_box.x_max)
               - min(first_bounding_box.x_min, second_bounding_box.x_min))
    delta_y = (max(first_bounding_box.y_max, second_bounding_box.y_max)
               - min(first_bounding_box.y_min, second_bounding_box.y_min))
    return first_polygon, Polygon([Contour([Point(point.x + 2 * delta_x,
                                                  point.y + 2 * delta_y)
                                            for point in contour.points],
                                           contour.holes, contour.is_external)
                                   for contour in second_polygon.contours])


def to_operation_with_non_overlapping_arguments(polygons_pair: Tuple[Polygon,
                                                                     Polygon],
                                                operation_type: OperationType
                                                ) -> Operation:
    return Operation(*polygons_pair, operation_type)


trivial_operations = (
        strategies.builds(Operation, empty_polygons, polygons,
                          operations_types)
        | strategies.builds(Operation, polygons, empty_polygons,
                            operations_types)
        | strategies.builds(to_operation_with_non_overlapping_arguments,
                            strategies.builds(to_non_overlapping_polygons_pair,
                                              non_empty_polygons,
                                              non_empty_polygons),
                            operations_types))
operations = strategies.builds(Operation, non_empty_polygons,
                               non_empty_polygons, operations_types)
operations |= trivial_operations


def to_operation_with_events_list(operation: Operation
                                  ) -> Tuple[Operation, List[SweepEvent]]:
    operation.process_segments()
    return operation, Operation.collect_events(operation.events)


operations_with_events_lists = (
        strategies.tuples(operations, strategies.builds(list))
        | operations.map(to_operation_with_events_list))
