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
                              to_nested_bound_sweep_events)
from tests.utils import (Strategy,
                         are_non_overlapping_sweep_events_pair,
                         are_sweep_events_pair_with_different_polygon_types,
                         is_sweep_event_non_degenerate,
                         to_valid_coordinates)

points = strategies.builds(Point, floats, floats)
sweep_events = to_bound_sweep_events()
nested_sweep_events = to_nested_bound_sweep_events()
maybe_nested_sweep_events = strategies.none() | nested_sweep_events
non_empty_sweep_events_lists = strategies.lists(sweep_events,
                                                min_size=1)


def to_sweep_events_lists_with_indices_and_booleans_lists(
        events: List[SweepEvent]
) -> Strategy[Tuple[List[SweepEvent], int, List[bool]]]:
    return strategies.tuples(strategies.just(events),
                             strategies.integers(0, len(events) - 1),
                             strategies.lists(booleans,
                                              min_size=len(events),
                                              max_size=len(events)))


non_empty_sweep_events_lists_with_indices_and_booleans_lists = (
    non_empty_sweep_events_lists.flatmap(
            to_sweep_events_lists_with_indices_and_booleans_lists))
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
coordinates = (strategies.lists(floats,
                                min_size=2,
                                max_size=2,
                                unique=True)
               .map(sorted)
               .map(tuple)
               .map(to_valid_coordinates))


def to_rectangle(xs: Tuple[float, float],
                 ys: Tuple[float, float]) -> List[Point]:
    min_x, max_x = xs
    min_y, max_y = ys
    return [Point(min_x, min_y), Point(max_x, min_y),
            Point(max_x, max_y), Point(min_x, max_y)]


rectangles_vertices = strategies.builds(to_rectangle, coordinates, coordinates)
contours_vertices = rectangles_vertices
contours = strategies.builds(Contour, contours_vertices,
                             strategies.builds(list), strategies.just(True))
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
non_trivial_operations = strategies.builds(Operation, non_empty_polygons,
                                           non_empty_polygons,
                                           operations_types)
operations = trivial_operations | non_trivial_operations


def pre_process_operation(operation: Operation) -> Operation:
    operation.process_segments()
    return operation


pre_processed_operations = operations.map(pre_process_operation)
pre_processed_non_trivial_operations = (non_trivial_operations
                                        .map(pre_process_operation))


def to_operation_with_events_list(operation: Operation
                                  ) -> Tuple[Operation, List[SweepEvent]]:
    return operation, Operation.collect_events(operation.sweep())


operations_with_events_lists = (
        strategies.tuples(operations, strategies.builds(list))
        | pre_processed_operations.map(to_operation_with_events_list))
