from typing import (List,
                    Tuple)

from hypothesis import strategies

from tests.bind_tests.utils import (BoundOperation,
                                    BoundOperationType,
                                    BoundPolygon,
                                    BoundSweepEvent,
                                    are_non_overlapping_bound_sweep_events)
from tests.integration_tests.factories import (
    make_cyclic_bound_with_ported_sweep_events,
    to_bound_with_ported_contours_pair,
    to_bound_with_ported_contours_vertices_pair,
    to_bound_with_ported_points_pair,
    to_bound_with_ported_polygons_pair,
    to_bound_with_ported_sweep_events)
from tests.integration_tests.utils import to_non_overlapping_contours_lists
from tests.port_tests.utils import (PortedOperation,
                                    PortedOperationType,
                                    PortedPolygon,
                                    PortedSweepEvent)
from tests.strategies import (booleans,
                              bound_with_ported_operations_types_pairs,
                              single_precision_floats as floats)
from tests.utils import (MAX_CONTOURS_COUNT,
                         MAX_NESTING_DEPTH,
                         Strategy,
                         are_sweep_events_pair_with_different_polygon_types,
                         to_double_nested_sweep_event,
                         to_pairs,
                         transpose)

booleans = booleans
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
nones_pairs = to_pairs(strategies.none())
leaf_sweep_events_pairs = to_bound_with_ported_sweep_events(nones_pairs)
acyclic_sweep_events_pairs = strategies.recursive(
        leaf_sweep_events_pairs, to_bound_with_ported_sweep_events,
        max_leaves=MAX_NESTING_DEPTH)
sweep_events_pairs = make_cyclic_bound_with_ported_sweep_events(
        acyclic_sweep_events_pairs)
nested_sweep_events_pairs = to_bound_with_ported_sweep_events(
        sweep_events_pairs)


def to_double_nested_sweep_events_pair(events_pair: Tuple[BoundSweepEvent,
                                                          PortedSweepEvent]
                                       ) -> Tuple[BoundSweepEvent,
                                                  PortedSweepEvent]:
    bound, ported = events_pair
    to_double_nested_sweep_event(bound)
    to_double_nested_sweep_event(ported)
    return bound, ported


double_nested_sweep_events_pairs = (nested_sweep_events_pairs
                                    .map(to_double_nested_sweep_events_pair))
maybe_nested_sweep_events_pairs = nones_pairs | nested_sweep_events_pairs
non_empty_sweep_events_lists_pairs = (strategies.lists(sweep_events_pairs,
                                                       min_size=1)
                                      .map(transpose))


def to_sweep_events_lists_pairs_with_indices_and_booleans_lists(
        events_pairs: Tuple[List[BoundSweepEvent], List[PortedSweepEvent]]
) -> Strategy[Tuple[List[BoundSweepEvent], List[PortedSweepEvent],
                    int, List[bool]]]:
    events_count = len(events_pairs[0])
    return strategies.tuples(strategies.just(events_pairs),
                             strategies.integers(0, events_count - 1),
                             strategies.lists(booleans,
                                              min_size=events_count,
                                              max_size=events_count))


non_empty_sweep_events_lists_pairs_with_indices_and_booleans_lists = (
    non_empty_sweep_events_lists_pairs.flatmap(
            to_sweep_events_lists_pairs_with_indices_and_booleans_lists))
nested_sweep_events_lists_pairs = (strategies.lists(nested_sweep_events_pairs)
                                   .map(transpose))
nested_sweep_events_pairs_pairs = (to_pairs(nested_sweep_events_pairs)
                                   .map(transpose))


def are_non_overlapping_sweep_events_pair_pair(
        events_pair_pair: Tuple[Tuple[BoundSweepEvent, BoundSweepEvent],
                                Tuple[PortedSweepEvent, PortedSweepEvent]]
) -> bool:
    bound_events_pair, ported_events_pair = events_pair_pair
    return (are_non_overlapping_bound_sweep_events(bound_events_pair)
            and
            are_non_overlapping_bound_sweep_events(ported_events_pair))


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
contours_vertices_pairs = to_bound_with_ported_contours_vertices_pair(floats)
contours_pairs = strategies.builds(to_bound_with_ported_contours_pair,
                                   contours_vertices_pairs,
                                   strategies.builds(list),
                                   strategies.just(True))
contours_lists_pairs = (strategies.lists(contours_pairs,
                                         max_size=MAX_CONTOURS_COUNT)
                        .map(transpose)
                        .map(to_non_overlapping_contours_lists))
empty_contours_lists_pairs = to_pairs(strategies.builds(list))
non_empty_contours_lists_pairs = (strategies.lists(contours_pairs,
                                                   min_size=1,
                                                   max_size=1)
                                  .map(transpose)
                                  .map(to_non_overlapping_contours_lists))
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
) -> Tuple[BoundOperation, PortedOperation]:
    bound_left, ported_left = left_polygons_pair
    bound_right, ported_right = right_polygons_pair
    (bound_operation_type,
     ported_operation_type) = operations_types_pair
    return (BoundOperation(bound_left, bound_right, bound_operation_type),
            PortedOperation(ported_left, ported_right, ported_operation_type))


operations_pairs = strategies.builds(to_bound_with_ported_operations_pair,
                                     polygons_pairs, polygons_pairs,
                                     operations_types_pairs)
non_trivial_operations_pairs = strategies.builds(
        to_bound_with_ported_operations_pair,
        non_empty_polygons_pairs, non_empty_polygons_pairs,
        operations_types_pairs)


def to_pre_processed_operations_pair(operations: Tuple[BoundOperation,
                                                       PortedOperation]
                                     ) -> Tuple[BoundOperation,
                                                PortedOperation]:
    bound, ported = operations
    bound.process_segments()
    ported.process_segments()
    return operations


pre_processed_operations_pairs = (operations_pairs
                                  .map(to_pre_processed_operations_pair))
pre_processed_non_trivial_operations_pairs = (
    non_trivial_operations_pairs.map(to_pre_processed_operations_pair))


def to_operations_with_events_lists_pair(
        operations: Tuple[BoundOperation, PortedOperation]
) -> Tuple[Tuple[BoundOperation, PortedOperation],
           Tuple[List[BoundSweepEvent], List[PortedSweepEvent]]]:
    bound, ported = operations
    return operations, (BoundOperation.collect_events(bound.sweep()),
                        PortedOperation.collect_events(ported.sweep()))


operations_with_events_lists_pairs = (
        strategies.tuples(operations_pairs,
                          to_pairs(strategies.builds(list)))
        | (pre_processed_operations_pairs
           .map(to_operations_with_events_lists_pair)))
