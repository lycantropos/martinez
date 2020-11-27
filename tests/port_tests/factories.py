from functools import partial
from itertools import repeat
from typing import (Any,
                    List,
                    Optional)

from hypothesis import strategies

from martinez.hints import Scalar
from tests.port_tests.utils import (PortedContour,
                                    PortedPoint,
                                    PortedPointsPair,
                                    PortedPointsTriplet,
                                    PortedPolygon,
                                    PortedPolygonType,
                                    PortedSegment,
                                    PortedSweepEvent,
                                    to_non_overlapping_ported_contours_list,
                                    to_ported_rectangle)
from tests.strategies import (booleans,
                              non_negative_integers,
                              non_negative_integers_lists,
                              ported_edges_types,
                              ported_polygons_types)
from tests.utils import (MAX_CONTOURS_COUNT,
                         MAX_NESTING_DEPTH,
                         Strategy,
                         compose,
                         make_cyclic,
                         to_valid_coordinates_pairs)


def scalars_to_ported_points(scalars: Strategy[Scalar]
                             ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, scalars, scalars)


def scalars_to_ported_points_pairs(scalars: Strategy[Scalar]
                                   ) -> Strategy[PortedPointsPair]:
    points_strategy = strategies.builds(PortedPoint, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy)


def scalars_to_ported_points_triplets(scalars: Strategy[Scalar]
                                      ) -> Strategy[PortedPointsTriplet]:
    points_strategy = strategies.builds(PortedPoint, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy, points_strategy)


def scalars_to_ported_points_lists(scalars: Strategy[Scalar],
                                   *,
                                   min_size: int = 0,
                                   max_size: Optional[int] = None
                                   ) -> Strategy[List[PortedPoint]]:
    return strategies.lists(scalars_to_ported_points(scalars),
                            min_size=min_size,
                            max_size=max_size)


def scalars_to_ported_polygons(scalars: Strategy[Scalar],
                               *,
                               min_size: int = 0,
                               max_size: Optional[int] = MAX_CONTOURS_COUNT
                               ) -> Strategy[PortedPolygon]:
    contours_lists = scalars_to_ported_contours_lists(scalars,
                                                      min_size=min_size,
                                                      max_size=max_size)
    return strategies.builds(PortedPolygon, contours_lists)


def scalars_to_ported_contours_lists(
        scalars: Strategy[Scalar],
        *,
        min_size: int = 0,
        max_size: Optional[int] = MAX_CONTOURS_COUNT
) -> Strategy[List[PortedContour]]:
    contours = scalars_to_ported_contours(scalars)
    return (strategies.lists(contours,
                             min_size=min_size,
                             max_size=max_size)
            .map(to_non_overlapping_ported_contours_list))


def scalars_to_ported_contours(scalars: Strategy[Scalar]
                               ) -> Strategy[PortedContour]:
    return strategies.builds(PortedContour,
                             scalars_to_ported_contours_vertices(scalars),
                             non_negative_integers_lists, booleans)


def scalars_to_ported_contours_vertices(scalars: Strategy[Scalar]
                                        ) -> Strategy[List[PortedPoint]]:
    coordinates = (strategies.lists(scalars,
                                    min_size=2)
                   .map(sorted)
                   .map(to_valid_coordinates_pairs))
    return strategies.builds(to_ported_rectangle, coordinates, coordinates)


def scalars_to_ported_segments(scalars: Strategy[Scalar]
                               ) -> Strategy[PortedSegment]:
    points_strategy = scalars_to_ported_points(scalars)
    return strategies.builds(PortedSegment, points_strategy, points_strategy)


def scalars_to_plain_ported_sweep_events(
        scalars: Strategy[Scalar],
        children: Strategy[Optional[PortedSweepEvent]],
        *,
        polygons_types: Strategy[PortedPolygonType] = ported_polygons_types
) -> Strategy[PortedSweepEvent]:
    return strategies.builds(PortedSweepEvent, booleans,
                             scalars_to_ported_points(scalars), children,
                             polygons_types, ported_edges_types,
                             booleans, booleans, booleans, booleans,
                             non_negative_integers, non_negative_integers,
                             children)


def scalars_to_acyclic_ported_sweep_events(scalars: Strategy[Scalar],
                                           *,
                                           min_depth: int = 1,
                                           max_depth: int = MAX_NESTING_DEPTH,
                                           **kwargs: Any
                                           ) -> Strategy[PortedSweepEvent]:
    events_factory = partial(scalars_to_plain_ported_sweep_events, scalars,
                             **kwargs)
    base = compose(*repeat(events_factory,
                           times=min_depth))(strategies.none())
    return strategies.recursive(base, events_factory,
                                max_leaves=max_depth - min_depth)


def scalars_to_ported_sweep_events(scalars: Strategy[Scalar],
                                   *,
                                   min_depth: int = 1,
                                   max_depth: int = MAX_NESTING_DEPTH,
                                   **kwargs: Any
                                   ) -> Strategy[PortedSweepEvent]:
    acyclic_events = scalars_to_acyclic_ported_sweep_events(
            scalars,
            min_depth=min_depth,
            max_depth=max_depth,
            **kwargs)
    return make_cyclic(acyclic_events)


scalars_to_nested_ported_sweep_events = partial(scalars_to_ported_sweep_events,
                                                min_depth=2)
