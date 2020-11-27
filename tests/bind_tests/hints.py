from typing import Tuple

from tests.bind_tests.hints import (BoundEventsQueueKey as BoundEventsQueueKey,
                                    BoundOperation as BoundOperation,
                                    BoundOperationType as BoundOperationType,
                                    BoundPoint as BoundPoint,
                                    BoundPolygon as BoundPolygon,
                                    BoundPolygonType as BoundPolygonType,
                                    BoundSweepEvent as BoundSweepEvent,
                                    BoundingBox as BoundBoundingBox,
                                    Contour as BoundContour,
                                    BoundEdgeType as BoundEdgeType,
                                    BoundSegment as BoundSegment,
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
