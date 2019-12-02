from _martinez import (BoundingBox as BoundBoundingBox,
                       Point as BoundPoint,
                       Segment as BoundSegment)
from hypothesis.searchstrategy import SearchStrategy

from martinez.bounding_box import BoundingBox as PortedBoundingBox
from martinez.point import Point as PortedPoint
from martinez.segment import Segment as PortedSegment

Strategy = SearchStrategy


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def are_bound_ported_bounding_boxes_equal(
        bound_bounding_box: BoundBoundingBox,
        ported_bounding_box: PortedBoundingBox) -> bool:
    return (bound_bounding_box.x_min == ported_bounding_box.x_min
            and bound_bounding_box.y_min == ported_bounding_box.y_min
            and bound_bounding_box.x_max == ported_bounding_box.x_max
            and bound_bounding_box.y_max == ported_bounding_box.y_max)


def are_bound_ported_points_equal(bound_point: BoundPoint,
                                  ported_point: PortedPoint) -> bool:
    return bound_point.x == ported_point.x and bound_point.y == ported_point.y


def are_bound_ported_segments_equal(bound_segment: BoundSegment,
                                    ported_segment: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound_segment.source,
                                          ported_segment.source)
            and are_bound_ported_points_equal(bound_segment.target,
                                              ported_segment.target))
