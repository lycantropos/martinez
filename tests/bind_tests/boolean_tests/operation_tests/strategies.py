from typing import (List,
                    Tuple)

from hypothesis import strategies

from tests.bind_tests.factories import (to_bound_contours,
                                        to_bound_sweep_events,
                                        to_nested_bound_sweep_events)
from tests.bind_tests.hints import (BoundOperation,
                                    BoundOperationType,
                                    BoundPoint,
                                    BoundPolygon,
                                    BoundSweepEvent)
from tests.bind_tests.utils import (are_non_overlapping_bound_sweep_events,
                                    bound_operations_types,
                                    to_non_overlapping_bound_contours_list,
                                    to_non_overlapping_bound_polygons_pair)
from tests.strategies import (booleans,
                              floats)
from tests.utils import (MAX_CONTOURS_COUNT,
                         Strategy,
                         are_sweep_events_pair_with_different_polygon_types,
                         is_sweep_event_non_degenerate,
                         to_double_nested_sweep_events)

points = strategies.builds(BoundPoint, floats, floats)
sweep_events = to_bound_sweep_events()
nested_sweep_events = to_nested_bound_sweep_events()
double_nested_sweep_events = to_double_nested_sweep_events(nested_sweep_events)
maybe_nested_sweep_events = strategies.none() | nested_sweep_events
non_empty_sweep_events_lists = strategies.lists(sweep_events,
                                                min_size=1)


def to_sweep_events_lists_with_indices_and_booleans_lists(
        events: List[BoundSweepEvent]
) -> Strategy[Tuple[List[BoundSweepEvent], int, List[bool]]]:
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
        .filter(are_non_overlapping_bound_sweep_events)
        | nested_sweep_events_pairs
        .filter(are_sweep_events_pair_with_different_polygon_types))
operations_types = bound_operations_types
contours = to_bound_contours()
contours_lists = (strategies.lists(contours,
                                   max_size=MAX_CONTOURS_COUNT)
                  .map(to_non_overlapping_bound_contours_list))
empty_contours_lists = strategies.builds(list)
non_empty_contours_lists = (strategies.lists(contours,
                                             min_size=1)
                            .map(to_non_overlapping_bound_contours_list))
polygons = strategies.builds(BoundPolygon, contours_lists)
empty_polygons = strategies.builds(BoundPolygon, empty_contours_lists)
non_empty_polygons = strategies.builds(BoundPolygon, non_empty_contours_lists)


def to_operation_with_non_overlapping_arguments(
        polygons_pair: Tuple[BoundPolygon,
                             BoundPolygon],
        operation_type: BoundOperationType
) -> BoundOperation:
    return BoundOperation(*polygons_pair, operation_type)


trivial_operations = (
        strategies.builds(BoundOperation, empty_polygons, polygons,
                          operations_types)
        | strategies.builds(BoundOperation, polygons, empty_polygons,
                            operations_types)
        | strategies.builds(to_operation_with_non_overlapping_arguments,
                            strategies.builds(
                                    to_non_overlapping_bound_polygons_pair,
                                    non_empty_polygons,
                                    non_empty_polygons),
                            operations_types))
non_trivial_operations = strategies.builds(BoundOperation, non_empty_polygons,
                                           non_empty_polygons,
                                           operations_types)
operations = trivial_operations | non_trivial_operations


def pre_process_operation(operation: BoundOperation) -> BoundOperation:
    operation.process_segments()
    return operation


pre_processed_operations = operations.map(pre_process_operation)
pre_processed_non_trivial_operations = (non_trivial_operations
                                        .map(pre_process_operation))


def to_operation_with_events_list(operation: BoundOperation
                                  ) -> Tuple[
    BoundOperation, List[BoundSweepEvent]]:
    return operation, BoundOperation.collect_events(operation.sweep())


operations_with_events_lists = (
        strategies.tuples(operations, strategies.builds(list))
        | pre_processed_operations.map(to_operation_with_events_list))
