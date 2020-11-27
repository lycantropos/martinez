from typing import (List,
                    Sequence,
                    Tuple)

from martinez.boolean import (EdgeType as PortedEdgeType,
                              EventsQueueKey as PortedEventsQueueKey,
                              Operation as PortedOperation,
                              OperationType as PortedOperationType,
                              PolygonType as PortedPolygonType,
                              SweepEvent as PortedSweepEvent,
                              SweepLineKey as PortedSweepLineKey)
from martinez.bounding_box import BoundingBox as PortedBoundingBox
from martinez.contour import Contour as PortedContour
from martinez.hints import Scalar
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from martinez.segment import Segment as PortedSegment
from martinez.utilities import find_intersections as ported_find_intersections
from tests.utils import to_bounding_boxes_offset

PortedBoundingBox = PortedBoundingBox
PortedContour = PortedContour
PortedEdgeType = PortedEdgeType
PortedEventsQueueKey = PortedEventsQueueKey
PortedOperation = PortedOperation
PortedOperationType = PortedOperationType
PortedPoint = PortedPoint
PortedPointsPair = Tuple[PortedPoint, PortedPoint]
PortedPointsTriplet = Tuple[PortedPoint, PortedPoint, PortedPoint]
PortedPolygon = PortedPolygon
PortedPolygonType = PortedPolygonType
PortedSegment = PortedSegment
PortedSweepEvent = PortedSweepEvent
PortedSweepLineKey = PortedSweepLineKey


def to_ported_rectangle(xs: Tuple[Scalar, Scalar],
                        ys: Tuple[Scalar, Scalar]) -> List[PortedPoint]:
    min_x, max_x = xs
    min_y, max_y = ys
    return [PortedPoint(min_x, min_y), PortedPoint(max_x, min_y),
            PortedPoint(max_x, max_y), PortedPoint(min_x, max_y)]


def are_non_overlapping_ported_segments(first_segment: PortedSegment,
                                        second_segment: PortedSegment) -> bool:
    return ported_find_intersections(first_segment, second_segment)[0] != 2


def to_non_overlapping_ported_contours_list(contours: List[PortedContour]
                                            ) -> List[PortedContour]:
    result = []
    previous_segments = []
    for contour in contours:
        segments = to_ported_segments(contour.points)
        if all(are_non_overlapping_ported_segments(segment, previous_segment)
               for segment in segments
               for previous_segment in previous_segments):
            result.append(contour)
            previous_segments.extend(segments)
    return result


def to_ported_segments(points: List[PortedPoint]) -> Sequence[PortedSegment]:
    return [PortedSegment(points[index], points[(index + 1) % len(points)])
            for index in range(len(points))]


def to_non_overlapping_ported_polygons_pair(first_polygon: PortedPolygon,
                                            second_polygon: PortedPolygon
                                            ) -> Tuple[PortedPolygon,
                                                       PortedPolygon]:
    delta_x, delta_y = to_bounding_boxes_offset(first_polygon.bounding_box,
                                                second_polygon.bounding_box)
    second_polygon = PortedPolygon(
            [PortedContour([PortedPoint(point.x + 2 * delta_x,
                                        point.y + 2 * delta_y)
                            for point in contour.points],
                           contour.holes, contour.is_external)
             for contour in second_polygon.contours])
    return first_polygon, second_polygon
