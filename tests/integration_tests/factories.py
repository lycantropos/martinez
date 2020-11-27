from typing import (Dict,
                    List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from tests.bind_tests.hints import (BoundContour,
                                    BoundEdgeType,
                                    BoundPoint,
                                    BoundPolygon,
                                    BoundPolygonType,
                                    BoundSegment,
                                    BoundSweepEvent)
from tests.bind_tests.utils import to_bound_rectangle
from tests.port_tests.hints import (PortedContour,
                                    PortedEdgeType,
                                    PortedPoint,
                                    PortedPolygon,
                                    PortedPolygonType,
                                    PortedSegment,
                                    PortedSweepEvent)
from tests.port_tests.utils import to_ported_rectangle
from tests.strategies import (booleans,
                              floats,
                              single_precision_floats,
                              unsigned_integers)
from tests.utils import (Strategy,
                         to_left_relinked_sweep_event,
                         to_links,
                         to_right_relinked_sweep_event,
                         to_valid_coordinates_pairs,
                         traverse_sweep_event)
from .hints import (BoundPortedPointsPair,
                    BoundPortedSweepEventsPair)
from .utils import (bound_with_ported_edges_types_pairs,
                    bound_with_ported_polygons_types_pairs)


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_contours_vertices_pair(
        coordinates: Strategy[float] = floats
) -> Strategy[Tuple[List[BoundPoint], List[PortedPoint]]]:
    coordinates_pairs = (strategies.lists(coordinates,
                                          min_size=2)
                         .map(sorted)
                         .map(to_valid_coordinates_pairs))

    def to_bound_with_ported_rectangles_pair(xs: Tuple[float, float],
                                             ys: Tuple[float, float]
                                             ) -> Tuple[List[BoundPoint],
                                                        List[PortedPoint]]:
        return to_bound_rectangle(xs, ys), to_ported_rectangle(xs, ys)

    rectangles_vertices_pairs = strategies.builds(
            to_bound_with_ported_rectangles_pair,
            coordinates_pairs, coordinates_pairs)
    return rectangles_vertices_pairs


def to_bound_with_ported_contours_pair(
        bound_with_ported_vertices_pair: Tuple[List[BoundPoint],
                                               List[PortedPoint]],
        holes: List[int],
        is_external: bool) -> Tuple[BoundContour, PortedContour]:
    bound_vertices, ported_vertices = bound_with_ported_vertices_pair
    return (BoundContour(bound_vertices, holes, is_external),
            PortedContour(ported_vertices, holes, is_external))


def to_bound_with_ported_segments_pair(
        bound_with_ported_sources_pair: BoundPortedPointsPair,
        bound_with_ported_targets_pair: BoundPortedPointsPair
) -> Tuple[BoundSegment, PortedSegment]:
    bound_source, ported_source = bound_with_ported_sources_pair
    bound_target, ported_target = bound_with_ported_targets_pair

    return (BoundSegment(bound_source, bound_target),
            PortedSegment(ported_source, ported_target))


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
        results_in_outs: Strategy[bool] = booleans,
        positions: Strategy[int] = unsigned_integers,
        contours_ids: Strategy[int] = unsigned_integers
) -> Strategy[BoundPortedSweepEventsPair]:
    def to_sweep_events(
            is_left: bool,
            points_pair: BoundPortedPointsPair,
            other_events_pair: Tuple[Optional[BoundSweepEvent],
                                     Optional[PortedSweepEvent]],
            polygons_types_pair: Tuple[BoundPolygonType, PortedPolygonType],
            edges_types_pair: Tuple[BoundEdgeType, PortedEdgeType],
            in_out: bool,
            other_in_out: bool,
            in_result: bool,
            result_in_out: bool,
            position: int,
            contour_id: int,
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
                                bound_polygon_type, bound_edge_type, in_out,
                                other_in_out, in_result, result_in_out,
                                position, contour_id,
                                bound_prev_in_result_event)
        ported = PortedSweepEvent(is_left, ported_point, ported_other_event,
                                  ported_polygon_type, ported_edge_type,
                                  in_out, other_in_out, in_result,
                                  result_in_out, position, contour_id,
                                  ported_prev_in_result_event)
        return bound, ported

    return strategies.builds(to_sweep_events,
                             are_left, points_pairs, children,
                             polygons_types_pairs, edges_types_pairs,
                             in_outs, other_in_outs, in_results,
                             results_in_outs, positions, contours_ids,
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


def to_bound_with_ported_polygons_pair(
        bound_with_ported_contours_lists_pair: Tuple[List[BoundContour],
                                                     List[PortedContour]]
) -> Tuple[BoundPolygon, PortedPolygon]:
    bound_contours, ported_contours = bound_with_ported_contours_lists_pair
    return BoundPolygon(bound_contours), PortedPolygon(ported_contours)
