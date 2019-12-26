from functools import partial
from typing import (Any,
                    Dict,
                    List,
                    Optional,
                    Tuple,
                    TypeVar)

from _martinez import (Contour as BoundContour,
                       EdgeType as BoundEdgeType,
                       Point as BoundPoint,
                       Polygon as BoundPolygon,
                       PolygonType as BoundPolygonType,
                       Segment as BoundSegment,
                       SweepEvent as BoundSweepEvent)
from hypothesis import strategies

from martinez.boolean import (EdgeType as PortedEdgeType,
                              PolygonType as PortedPolygonType,
                              SweepEvent as PortedSweepEvent)
from martinez.contour import Contour as PortedContour
from martinez.hints import Scalar
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from martinez.segment import Segment as PortedSegment
from tests.utils import (BoundPortedPointsPair,
                         BoundPortedSweepEventsPair,
                         PortedPointsPair,
                         PortedPointsTriplet,
                         Strategy,
                         traverse_sweep_event)
from .literals import (booleans,
                       bound_edges_types,
                       bound_polygons_types,
                       bound_with_ported_edges_types_pairs,
                       bound_with_ported_polygons_types_pairs,
                       floats,
                       non_negative_integers,
                       ported_edges_types,
                       ported_polygons_types,
                       single_precision_floats,
                       unsigned_integers)


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


def scalars_to_ported_segments(scalars: Strategy[Scalar]
                               ) -> Strategy[PortedSegment]:
    points_strategy = scalars_to_ported_points(scalars)
    return strategies.builds(PortedSegment, points_strategy, points_strategy)


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_contours_pair(
        bound_with_ported_points_lists_pair: Tuple[List[BoundPoint],
                                                   List[PortedPoint]],
        holes: List[int],
        is_external: bool) -> Tuple[BoundContour, PortedContour]:
    bound_points, ported_points = bound_with_ported_points_lists_pair
    return (BoundContour(bound_points, holes, is_external),
            PortedContour(ported_points, holes, is_external))


def to_bound_with_ported_segments_pair(
        bound_with_ported_sources_pair: BoundPortedPointsPair,
        bound_with_ported_targets_pair: BoundPortedPointsPair
) -> Tuple[BoundSegment, PortedSegment]:
    bound_source, ported_source = bound_with_ported_sources_pair
    bound_target, ported_target = bound_with_ported_targets_pair

    return (BoundSegment(bound_source, bound_target),
            PortedSegment(ported_source, ported_target))


AnySweepEvent = TypeVar('AnySweepEvent', PortedSweepEvent, BoundSweepEvent)


def make_cyclic(sweep_events: Strategy[AnySweepEvent]
                ) -> Strategy[AnySweepEvent]:
    def to_cyclic_sweep_events(sweep_event: AnySweepEvent
                               ) -> Strategy[AnySweepEvent]:
        events = traverse_sweep_event(sweep_event, {}, {})
        links = to_links(len(events))
        return (strategies.builds(to_left_relinked_sweep_event,
                                  strategies.just(events), links)
                | strategies.builds(to_right_relinked_sweep_event,
                                    strategies.just(events), links))

    return sweep_events.flatmap(to_cyclic_sweep_events)


def to_links(events_count: int) -> Strategy[Dict[int, int]]:
    return strategies.dictionaries(strategies.integers(0, events_count - 1),
                                   strategies.integers(0, events_count - 1),
                                   min_size=events_count // 2)


def to_left_relinked_sweep_event(events: List[AnySweepEvent],
                                 links: Dict[int, int]) -> AnySweepEvent:
    for source, destination in links.items():
        events[source].other_event = events[destination]
    return events[0]


def to_right_relinked_sweep_event(events: List[AnySweepEvent],
                                  links: Dict[int, int]) -> AnySweepEvent:
    for source, destination in links.items():
        events[source].prev_in_result_event = events[destination]
    return events[0]


def to_bound_with_ported_sweep_events(
        children: Strategy[Tuple[Optional[BoundSweepEvent],
                                 Optional[PortedSweepEvent]]],
        are_left: Strategy[bool] = booleans,
        points_pairs: BoundPortedPointsPair = strategies.builds(
                to_bound_with_ported_points_pair, single_precision_floats,
                single_precision_floats),
        polygons_types_pairs: Strategy[Tuple[BoundPolygonType,
                                             PortedPolygonType]]
        = bound_with_ported_polygons_types_pairs,
        edges_types_pairs: Strategy[Tuple[BoundEdgeType, PortedEdgeType]]
        = bound_with_ported_edges_types_pairs,
        in_outs: Strategy[bool] = booleans,
        other_in_outs: Strategy[bool] = booleans,
        in_results: Strategy[bool] = booleans,
        positions: Strategy[int] = unsigned_integers
) -> Strategy[BoundPortedSweepEventsPair]:
    def to_sweep_events(
            is_left: bool, points_pair: BoundPortedPointsPair,
            other_events_pair: Tuple[Optional[BoundSweepEvent],
                                     Optional[PortedSweepEvent]],
            polygons_types_pair: Tuple[BoundPolygonType, PortedPolygonType],
            edges_types_pair: Tuple[BoundEdgeType, PortedEdgeType],
            in_out: bool, other_in_out: bool, in_result: bool, position: int,
            prev_in_result_events_pair: Tuple[Optional[BoundSweepEvent],
                                              Optional[PortedSweepEvent]]
    ) -> BoundPortedSweepEventsPair:
        bound_point, ported_point = points_pair
        bound_other_event, ported_other_event = other_events_pair
        bound_polygon_type, ported_polygon_type = polygons_types_pair
        bound_edge_type, ported_edge_type = edges_types_pair
        (bound_prev_in_result_event,
         ported_prev_in_result_event) = prev_in_result_events_pair
        bound = BoundSweepEvent(is_left, bound_point, bound_other_event,
                                bound_polygon_type, bound_edge_type,
                                in_out, other_in_out, in_result, position,
                                bound_prev_in_result_event)
        ported = PortedSweepEvent(is_left, ported_point, ported_other_event,
                                  ported_polygon_type, ported_edge_type,
                                  in_out, other_in_out, in_result, position,
                                  ported_prev_in_result_event)
        return bound, ported

    return strategies.builds(to_sweep_events,
                             are_left, points_pairs, children,
                             polygons_types_pairs, edges_types_pairs,
                             in_outs, other_in_outs, in_results, positions,
                             children)


def make_cyclic_bound_with_ported_sweep_events(
        sweep_events_pairs: Strategy[BoundPortedSweepEventsPair]
) -> Strategy[BoundPortedSweepEventsPair]:
    def to_cyclic_sweep_events_pair(
            sweep_events_pair: BoundPortedSweepEventsPair
    ) -> Strategy[BoundPortedSweepEventsPair]:
        bound, ported = sweep_events_pair
        bound_left_links, ported_left_links = {}, {}
        bound_right_links, ported_right_links = {}, {}
        bound_events = traverse_sweep_event(bound, bound_left_links,
                                            bound_right_links)
        ported_events = traverse_sweep_event(ported, ported_left_links,
                                             ported_right_links)
        links = to_links(len(bound_events))
        return (strategies.builds(to_left_relinked_sweep_events_pair,
                                  strategies.just(bound_events),
                                  strategies.just(ported_events),
                                  links)
                | strategies.builds(to_right_relinked_sweep_events_pair,
                                    strategies.just(bound_events),
                                    strategies.just(ported_events),
                                    links))

    def to_left_relinked_sweep_events_pair(
            bound_events: List[BoundSweepEvent],
            ported_events: List[PortedSweepEvent],
            links: Dict[int, int]) -> Tuple[BoundSweepEvent, PortedSweepEvent]:
        return (to_left_relinked_sweep_event(bound_events, links),
                to_left_relinked_sweep_event(ported_events, links))

    def to_right_relinked_sweep_events_pair(
            bound_events: List[BoundSweepEvent],
            ported_events: List[PortedSweepEvent],
            links: Dict[int, int]) -> Tuple[BoundSweepEvent, PortedSweepEvent]:
        return (to_right_relinked_sweep_event(bound_events, links),
                to_right_relinked_sweep_event(ported_events, links))

    return sweep_events_pairs.flatmap(to_cyclic_sweep_events_pair)


def scalars_to_plain_ported_sweep_events(
        scalars: Strategy[Scalar],
        children: Strategy[Optional[PortedSweepEvent]],
        *,
        polygons_types: Strategy[PortedPolygonType] = ported_polygons_types
) -> Strategy[PortedSweepEvent]:
    return strategies.builds(PortedSweepEvent, booleans,
                             scalars_to_ported_points(scalars), children,
                             polygons_types, ported_edges_types,
                             booleans, booleans, booleans,
                             non_negative_integers, children)


def scalars_to_acyclic_ported_sweep_events(
        scalars: Strategy[Scalar],
        children: Strategy[Optional[PortedSweepEvent]] = strategies.none(),
        **kwargs: Any
) -> Strategy[PortedSweepEvent]:
    events_factory = partial(scalars_to_plain_ported_sweep_events, scalars,
                             **kwargs)
    return strategies.recursive(events_factory(children), events_factory)


def scalars_to_nested_ported_sweep_events(scalars: Strategy[Scalar],
                                          **kwargs: Any
                                          ) -> Strategy[PortedSweepEvent]:
    acyclic_events = scalars_to_acyclic_nested_ported_sweep_events(scalars,
                                                                   **kwargs)
    return strategies.recursive(acyclic_events, make_cyclic)


def scalars_to_ported_sweep_events(scalars: Strategy[Scalar], **kwargs: Any
                                   ) -> Strategy[PortedSweepEvent]:
    acyclic_events = scalars_to_acyclic_ported_sweep_events(scalars, **kwargs)
    return strategies.recursive(acyclic_events, make_cyclic)


def scalars_to_acyclic_nested_ported_sweep_events(
        scalars: Strategy[Scalar],
        **kwargs: Any) -> Strategy[PortedSweepEvent]:
    events_factory = partial(scalars_to_acyclic_ported_sweep_events,
                             scalars, **kwargs)
    return events_factory(events_factory())


def to_plain_bound_sweep_events(
        children: Strategy[Optional[BoundSweepEvent]],
        *,
        polygons_types: Strategy[BoundPolygonType] = bound_polygons_types
) -> Strategy[BoundSweepEvent]:
    return strategies.builds(BoundSweepEvent, booleans,
                             strategies.builds(BoundPoint, floats, floats),
                             children, polygons_types, bound_edges_types,
                             booleans, booleans, booleans, unsigned_integers,
                             children)


def to_bound_sweep_events(**kwargs: Any) -> Strategy[PortedSweepEvent]:
    acyclic_events = to_acyclic_bound_sweep_events(strategies.none(), **kwargs)
    return strategies.recursive(acyclic_events, make_cyclic)


def to_nested_bound_sweep_events(**kwargs: Any) -> Strategy[PortedSweepEvent]:
    acyclic_events = to_acyclic_nested_bound_sweep_events(**kwargs)
    return strategies.recursive(acyclic_events, make_cyclic)


def to_acyclic_nested_bound_sweep_events(**kwargs: Any
                                         ) -> Strategy[BoundSweepEvent]:
    events_factory = partial(to_acyclic_bound_sweep_events, **kwargs)
    return events_factory(events_factory(strategies.none()))


def to_acyclic_bound_sweep_events(
        children: Strategy[Optional[BoundSweepEvent]],
        **kwargs: Any) -> Strategy[BoundSweepEvent]:
    events_factory = partial(to_plain_bound_sweep_events, **kwargs)
    return strategies.recursive(events_factory(children), events_factory)


def to_bound_with_ported_polygons_pair(
        bound_with_ported_contours_lists_pair: Tuple[List[BoundContour],
                                                     List[PortedContour]]
) -> Tuple[BoundPolygon, PortedPolygon]:
    bound_contours, ported_contours = bound_with_ported_contours_lists_pair
    return BoundPolygon(bound_contours), PortedPolygon(ported_contours)
