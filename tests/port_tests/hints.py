from typing import Tuple

from martinez.boolean import (EdgeType as PortedEdgeType,
                              EventsQueueKey as PortedEventsQueueKey,
                              Operation as PortedOperation,
                              OperationType as PortedOperationType,
                              PolygonType as PortedPolygonType,
                              SweepEvent as PortedSweepEvent,
                              SweepLineKey as PortedSweepLineKey)
from martinez.bounding_box import BoundingBox as PortedBoundingBox
from martinez.contour import Contour as PortedContour
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from martinez.segment import Segment as PortedSegment

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
