from typing import (List,
                    Sequence,
                    Tuple)

from _martinez import (BoundingBox as BoundBoundingBox,
                       Contour as BoundContour,
                       EdgeType as BoundEdgeType,
                       EventsQueueKey as BoundEventsQueueKey,
                       Operation as BoundOperation,
                       OperationType as BoundOperationType,
                       Point as BoundPoint,
                       Polygon as BoundPolygon,
                       PolygonType as BoundPolygonType,
                       Segment as BoundSegment,
                       SweepEvent as BoundSweepEvent,
                       SweepLineKey as BoundSweepLineKey,
                       find_intersections as bound_find_intersections)

from tests.utils import to_bounding_boxes_offset

BoundBoundingBox = BoundBoundingBox
BoundContour = BoundContour
BoundEdgeType = BoundEdgeType
BoundEventsQueueKey = BoundEventsQueueKey
BoundOperation = BoundOperation
BoundOperationType = BoundOperationType
BoundPoint = BoundPoint
BoundPolygon = BoundPolygon
BoundPolygonType = BoundPolygonType
BoundSegment = BoundSegment
BoundSweepEvent = BoundSweepEvent
BoundSweepLineKey = BoundSweepLineKey
BoundPointsPair = Tuple[BoundPoint, BoundPoint]
BoundPointsTriplet = Tuple[BoundPoint, BoundPoint, BoundPoint]


def to_bound_rectangle(xs: Tuple[float, float],
                       ys: Tuple[float, float]) -> List[BoundPoint]:
    min_x, max_x = xs
    min_y, max_y = ys
    return [BoundPoint(min_x, min_y), BoundPoint(max_x, min_y),
            BoundPoint(max_x, max_y), BoundPoint(min_x, max_y)]


def to_non_overlapping_bound_contours_list(contours: List[BoundContour]
                                           ) -> List[BoundContour]:
    result = []
    previous_segments = []
    for contour in contours:
        segments = to_bound_segments(contour.points)
        if all(are_non_overlapping_bound_segments(segment, previous_segment)
               for segment in segments
               for previous_segment in previous_segments):
            result.append(contour)
            previous_segments.extend(segments)
    return result


def to_bound_segments(points: List[BoundPoint]) -> Sequence[BoundSegment]:
    return [BoundSegment(points[index], points[(index + 1) % len(points)])
            for index in range(len(points))]


def to_non_overlapping_bound_polygons_pair(first_polygon: BoundPolygon,
                                           second_polygon: BoundPolygon
                                           ) -> Tuple[BoundPolygon,
                                                      BoundPolygon]:
    delta_x, delta_y = to_bounding_boxes_offset(first_polygon.bounding_box,
                                                second_polygon.bounding_box)
    second_polygon = BoundPolygon(
            [BoundContour([BoundPoint(point.x + 2 * delta_x,
                                      point.y + 2 * delta_y)
                           for point in contour.points],
                          contour.holes, contour.is_external)
             for contour in second_polygon.contours])
    return first_polygon, second_polygon


def are_non_overlapping_bound_sweep_events(events_pair: Tuple[BoundSweepEvent,
                                                              BoundSweepEvent]
                                           ) -> bool:
    first_event, second_event = events_pair
    first_segment, second_segment = first_event.segment, second_event.segment
    return are_non_overlapping_bound_segments(first_segment, second_segment)


def are_non_overlapping_bound_segments(first_segment: BoundSegment,
                                       second_segment: BoundSegment) -> bool:
    return bound_find_intersections(first_segment, second_segment)[0] != 2
