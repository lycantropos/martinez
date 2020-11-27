from typing import (List,
                    Sequence,
                    Tuple,
                    Union)

from tests.bind_tests.utils import (BoundBoundingBox,
                                    BoundContour,
                                    BoundEventsQueueKey,
                                    BoundOperation,
                                    BoundPoint,
                                    BoundPolygon,
                                    BoundSegment,
                                    BoundSweepEvent,
                                    BoundSweepLineKey,
                                    to_non_overlapping_bound_contours_list)
from tests.port_tests.utils import (PortedBoundingBox,
                                    PortedContour,
                                    PortedEventsQueueKey,
                                    PortedOperation,
                                    PortedPoint,
                                    PortedPolygon,
                                    PortedSegment,
                                    PortedSweepEvent,
                                    PortedSweepLineKey,
                                    to_non_overlapping_ported_contours_list)
from tests.utils import traverse_sweep_event

BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSweepEventsPair = Tuple[BoundSweepEvent, PortedSweepEvent]


def are_bound_ported_bounding_boxes_equal(bound: BoundBoundingBox,
                                          ported: PortedBoundingBox) -> bool:
    return (bound.x_min == ported.x_min and bound.y_min == ported.y_min
            and bound.x_max == ported.x_max and bound.y_max == ported.y_max)


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_points_sequences_equal(bound: Sequence[BoundPoint],
                                            ported: Sequence[PortedPoint]
                                            ) -> bool:
    return (len(bound) == len(ported)
            and all(map(are_bound_ported_points_equal, bound, ported)))


def are_bound_ported_segments_equal(bound: BoundSegment,
                                    ported: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound.source, ported.source)
            and are_bound_ported_points_equal(bound.target, ported.target))


def are_bound_ported_contours_equal(bound: BoundContour,
                                    ported: PortedContour) -> bool:
    return (are_bound_ported_points_sequences_equal(bound.points,
                                                    ported.points)
            and bound.holes == ported.holes
            and bound.is_external is ported.is_external)


def are_bound_ported_polygons_equal(bound: BoundPolygon,
                                    ported: PortedPolygon) -> bool:
    return (len(bound.contours) == len(ported.contours)
            and all(map(are_bound_ported_contours_equal,
                        bound.contours, ported.contours)))


def are_bound_ported_sweep_events_equal(bound: BoundSweepEvent,
                                        ported: PortedSweepEvent) -> bool:
    def are_fields_equal(bound: BoundSweepEvent,
                         ported: PortedSweepEvent) -> bool:
        return (bound.is_left is ported.is_left
                and are_bound_ported_points_equal(bound.point, ported.point)
                and bound.polygon_type == ported.polygon_type
                and bound.edge_type == ported.edge_type
                and bound.in_out is ported.in_out
                and bound.other_in_out is ported.other_in_out
                and bound.in_result is ported.in_result
                and bound.result_in_out is ported.result_in_out
                and bound.position == ported.position
                and bound.contour_id == ported.contour_id)

    bound_left_links, ported_left_links = {}, {}
    bound_right_links, ported_right_links = {}, {}
    bound_events = traverse_sweep_event(bound, bound_left_links,
                                        bound_right_links)
    ported_events = traverse_sweep_event(ported, ported_left_links,
                                         ported_right_links)
    return (bound_left_links == ported_left_links
            and bound_right_links == ported_right_links
            and len(bound_events) == len(ported_events)
            and all(map(are_fields_equal, bound_events, ported_events)))


def are_bound_ported_sweep_events_lists_equal(bound: List[BoundSweepEvent],
                                              ported: List[PortedSweepEvent]
                                              ) -> bool:
    return (len(bound) == len(ported)
            and all(map(are_bound_ported_sweep_events_equal, bound, ported)))


def are_bound_ported_events_queue_keys_equal(bound: BoundEventsQueueKey,
                                             ported: PortedEventsQueueKey
                                             ) -> bool:
    return are_bound_ported_sweep_events_equal(bound.event, ported.event)


def are_bound_ported_sweep_line_keys_equal(bound: BoundSweepLineKey,
                                           ported: PortedSweepLineKey
                                           ) -> bool:
    return are_bound_ported_sweep_events_equal(bound.event, ported.event)


def are_bound_ported_operations_equal(bound: BoundOperation,
                                      ported: PortedOperation) -> bool:
    return (are_bound_ported_polygons_equal(bound.left, ported.left)
            and are_bound_ported_polygons_equal(bound.right, ported.right)
            and bound.type == ported.type)


def are_bounding_boxes_empty(bounding_box: Union[BoundBoundingBox,
                                                 PortedBoundingBox]) -> bool:
    return not (bounding_box.x_min or bounding_box.y_min
                or bounding_box.x_max or bounding_box.y_max)


def to_non_overlapping_contours_lists(lists: Tuple[List[BoundContour],
                                                   List[PortedContour]]
                                      ) -> Tuple[List[BoundContour],
                                                 List[PortedContour]]:
    bound, ported = lists
    return (to_non_overlapping_bound_contours_list(bound),
            to_non_overlapping_ported_contours_list(ported))
