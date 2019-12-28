from functools import partial
from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from martinez.boolean import (Operation,
                              OperationType,
                              SweepEvent)
from martinez.contour import Contour
from martinez.hints import Scalar
from martinez.polygon import Polygon
from tests.strategies import (booleans,
                              non_negative_integers_lists,
                              ported_operations_types,
                              scalars_strategies,
                              scalars_to_nested_ported_sweep_events,
                              scalars_to_ported_points,
                              scalars_to_ported_sweep_events)
from tests.utils import (MAX_CONTOURS_COUNT,
                         Strategy,
                         are_non_overlapping_sweep_events_pair,
                         are_sweep_events_pair_with_different_polygon_types,
                         is_sweep_event_non_degenerate,
                         strategy_to_pairs,
                         to_non_overlapping_contours_list,
                         to_non_overlapping_ported_polygons_pair,
                         to_ported_rectangle,
                         to_valid_coordinates_pairs)

points = scalars_strategies.flatmap(scalars_to_ported_points)
sweep_events = scalars_strategies.flatmap(scalars_to_ported_sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
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
nested_sweep_events_pairs = (scalars_strategies
                             .map(scalars_to_nested_ported_sweep_events)
                             .flatmap(strategy_to_pairs))
nested_sweep_events_pairs = (
        nested_sweep_events_pairs
        .filter(are_non_overlapping_sweep_events_pair)
        | nested_sweep_events_pairs
        .filter(are_sweep_events_pair_with_different_polygon_types))
operations_types = ported_operations_types


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
            | strategies.builds(
                    to_operation_with_non_overlapping_arguments,
                    strategies.builds(to_non_overlapping_ported_polygons_pair,
                                      non_empty_polygons,
                                      non_empty_polygons),
                    operations_types))


def scalars_to_polygons(scalars: Strategy[Scalar],
                        *,
                        min_size: int = 0,
                        max_size: Optional[int] = MAX_CONTOURS_COUNT
                        ) -> Strategy[Polygon]:
    return strategies.builds(Polygon,
                             scalars_to_contours_lists(scalars,
                                                       min_size=min_size,
                                                       max_size=max_size))


polygons = scalars_strategies.flatmap(scalars_to_polygons)
non_empty_polygons = scalars_strategies.flatmap(partial(scalars_to_polygons,
                                                        min_size=1))


def scalars_to_contours_lists(scalars: Strategy[Scalar],
                              *,
                              min_size: int = 0,
                              max_size: Optional[int] = MAX_CONTOURS_COUNT
                              ) -> Strategy[List[Contour]]:
    contours = scalars_to_contours(scalars)
    return (strategies.lists(contours,
                             min_size=min_size,
                             max_size=max_size)
            .map(to_non_overlapping_contours_list))


def scalars_to_contours(scalars: Strategy[Scalar]) -> Strategy[Contour]:
    return strategies.builds(Contour, scalars_to_contours_vertices(scalars),
                             non_negative_integers_lists, booleans)


def scalars_to_contours_vertices(scalars: Strategy[Scalar]) -> List:
    coordinates = (strategies.lists(scalars,
                                    min_size=2)
                   .map(sorted)
                   .map(to_valid_coordinates_pairs))
    return strategies.builds(to_ported_rectangle, coordinates, coordinates)


trivial_operations = (scalars_strategies
                      .flatmap(partial(scalars_to_trivial_operations,
                                       operations_types=operations_types)))
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
