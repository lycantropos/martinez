from functools import partial
from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from martinez.boolean import (Operation,
                              OperationType)
from martinez.contour import Contour
from martinez.hints import Scalar
from martinez.point import Point
from martinez.polygon import Polygon
from tests.strategies import (booleans,
                              non_negative_integers_lists,
                              ported_operations_types,
                              scalars_strategies,
                              scalars_to_nested_ported_sweep_events,
                              scalars_to_ported_points,
                              scalars_to_ported_points_triplets,
                              scalars_to_ported_sweep_events)
from tests.utils import (Strategy,
                         are_non_overlapping_sweep_events_pair,
                         are_sweep_events_pair_with_different_polygon_types,
                         is_sweep_event_non_degenerate,
                         strategy_to_pairs,
                         vertices_form_strict_polygon)

points = scalars_strategies.flatmap(scalars_to_ported_points)
sweep_events = scalars_strategies.flatmap(scalars_to_ported_sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
nested_sweep_events_lists = strategies.lists(nested_sweep_events)
non_degenerate_nested_sweep_events = (nested_sweep_events
                                      .filter(is_sweep_event_non_degenerate))
nested_sweep_events_pairs = (scalars_strategies
                             .map(scalars_to_nested_ported_sweep_events)
                             .flatmap(strategy_to_pairs))
nested_sweep_events_pairs = (
        nested_sweep_events_pairs
        .filter(are_non_overlapping_sweep_events_pair)
        | nested_sweep_events_pairs
        .filter(are_sweep_events_pair_with_different_polygon_types))
operations_types = ported_operations_types


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


def scalars_to_operations(scalars: Strategy[Scalar],
                          operations_types: Strategy[OperationType]
                          ) -> Strategy[Operation]:
    polygons = scalars_to_polygons(scalars)
    return strategies.builds(Operation, polygons, polygons, operations_types)


def scalars_to_trivial_operations(scalars: Strategy[Scalar],
                                  operations_types: Strategy[OperationType]):
    empty_contours_lists = strategies.builds(list)
    empty_polygons = strategies.builds(Polygon, empty_contours_lists)
    polygons = scalars_to_polygons(scalars)
    non_empty_polygons = scalars_to_polygons(scalars,
                                             min_size=1)
    return (strategies.builds(Operation, empty_polygons, polygons,
                              operations_types)
            | strategies.builds(Operation, polygons, empty_polygons,
                                operations_types)
            | strategies.builds(to_operation_with_non_overlapping_arguments,
                                strategies.builds(
                                        to_non_overlapping_polygons_pair,
                                        non_empty_polygons,
                                        non_empty_polygons),
                                operations_types))


def scalars_to_polygons(scalars: Strategy[Scalar],
                        *,
                        min_size: int = 0,
                        max_size: Optional[int] = None
                        ) -> Strategy[Polygon]:
    return strategies.builds(Polygon,
                             scalars_to_contours_lists(scalars,
                                                       min_size=min_size,
                                                       max_size=max_size))


polygons = scalars_strategies.flatmap(scalars_to_polygons)


def scalars_to_contours_lists(scalars: Strategy[Scalar],
                              *,
                              min_size: int = 0,
                              max_size: Optional[int] = None
                              ) -> Strategy[List[Contour]]:
    contours = scalars_to_contours(scalars)
    return strategies.lists(contours,
                            min_size=min_size,
                            max_size=max_size)


def scalars_to_contours(scalars: Strategy[Scalar]) -> Strategy[Contour]:
    return strategies.builds(Contour, scalars_to_contours_vertices(scalars),
                             non_negative_integers_lists, booleans)


def scalars_to_contours_vertices(scalars: Strategy[Scalar]) -> List:
    return (scalars_to_ported_points_triplets(scalars)
            .filter(vertices_form_strict_polygon)
            .map(list))


trivial_operations = (scalars_strategies
                      .flatmap(partial(scalars_to_trivial_operations,
                                       operations_types=operations_types)))
operations = (scalars_strategies
              .flatmap(partial(scalars_to_operations,
                               operations_types=operations_types))
              | trivial_operations)
