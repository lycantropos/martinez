from typing import Tuple

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
                       SweepLineKey as BoundSweepLineKey)

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
