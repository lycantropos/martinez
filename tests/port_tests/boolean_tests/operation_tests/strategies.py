from typing import (List,
                    Tuple)

from hypothesis import strategies

from martinez.boolean import (Operation,
                              OperationType,
                              SweepEvent)
from martinez.hints import Scalar
from martinez.polygon import Polygon
from tests.strategies import (booleans,
                              ported_operations_types,
                              scalars_strategies)
from tests.port_tests.factories import scalars_to_nested_ported_sweep_events, \
    scalars_to_ported_points, \
    scalars_to_ported_polygons, scalars_to_ported_sweep_events
from tests.utils import (Strategy,
                         are_sweep_events_pair_with_different_polygon_types,
                         cleave_in_tuples,
                         compose,
                         identity,
                         is_sweep_event_non_degenerate,
                         to_double_nested_sweep_events, to_maybe,
                         to_pairs,
                         to_triplets)
from tests.port_tests.utils import to_non_overlapping_ported_polygons_pair
from tests.bind_tests.utils import are_non_overlapping_bound_sweep_events

points = scalars_strategies.flatmap(scalars_to_ported_points)
sweep_events = scalars_strategies.flatmap(scalars_to_ported_sweep_events)
nested_sweep_events = (scalars_strategies
                       .flatmap(scalars_to_nested_ported_sweep_events))
maybe_nested_sweep_events = to_maybe(nested_sweep_events)
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
                             .flatmap(to_pairs))
nested_sweep_events_pairs = (
        nested_sweep_events_pairs
        .filter(are_non_overlapping_bound_sweep_events)
        | nested_sweep_events_pairs
        .filter(are_sweep_events_pair_with_different_polygon_types))
operations_types = ported_operations_types
polygons = scalars_strategies.flatmap(scalars_to_ported_polygons)


def scalars_to_trivial_operations(scalars: Strategy[Scalar]
                                  ) -> Strategy[Operation]:
    empty_polygons = strategies.builds(Polygon, strategies.builds(list))
    polygons = scalars_to_ported_polygons(scalars)
    non_empty_polygons = scalars_to_ported_polygons(scalars,
                                                    min_size=1)

    def to_operation_with_non_overlapping_arguments(
            polygons_pair: Tuple[Polygon, Polygon],
            operation_type: OperationType) -> Operation:
        return Operation(*polygons_pair, operation_type)

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


def scalars_to_non_trivial_operations(scalars: Strategy[Scalar]
                                      ) -> Strategy[Operation]:
    non_empty_polygons = scalars_to_ported_polygons(scalars,
                                                    min_size=1)
    return strategies.builds(Operation, non_empty_polygons, non_empty_polygons,
                             operations_types)


def scalars_to_operations(scalars: Strategy[Scalar]) -> Strategy[Operation]:
    return (scalars_to_trivial_operations(scalars)
            | scalars_to_non_trivial_operations(scalars))


operations_strategies = scalars_strategies.map(scalars_to_operations)
operations = operations_strategies.flatmap(identity)
operations_with_sweep_events = scalars_strategies.flatmap(
        cleave_in_tuples(scalars_to_operations,
                         scalars_to_ported_sweep_events))
operations_with_double_nested_sweep_events_and_points = (
    scalars_strategies.flatmap(
            cleave_in_tuples(scalars_to_operations,
                             compose(to_double_nested_sweep_events,
                                     scalars_to_nested_ported_sweep_events),
                             scalars_to_ported_points)))
operations_with_sweep_events_and_maybe_sweep_events = (
    scalars_strategies.flatmap(
            cleave_in_tuples(scalars_to_operations,
                             scalars_to_ported_sweep_events,
                             compose(to_maybe,
                                     scalars_to_nested_ported_sweep_events))))
operations_pairs = operations_strategies.flatmap(to_pairs)
operations_triplets = operations_strategies.flatmap(to_triplets)


def pre_process_operation(operation: Operation) -> Operation:
    operation.process_segments()
    return operation


pre_processed_operations = operations.map(pre_process_operation)
pre_processed_non_trivial_operations = (scalars_strategies
                                        .map(scalars_to_non_trivial_operations)
                                        .flatmap(identity)
                                        .map(pre_process_operation))


def to_operation_with_events_list(operation: Operation
                                  ) -> Tuple[Operation, List[SweepEvent]]:
    return operation, Operation.collect_events(operation.sweep())


operations_with_events_lists = (
        strategies.tuples(operations, strategies.builds(list))
        | pre_processed_operations.map(to_operation_with_events_list))
