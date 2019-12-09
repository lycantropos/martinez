from typing import (Any,
                    Hashable,
                    Iterable,
                    Sequence,
                    Tuple,
                    TypeVar,
                    Union)

from _martinez import (BoundingBox as BoundBoundingBox,
                       Contour as BoundContour,
                       Point as BoundPoint,
                       Polygon as BoundPolygon,
                       Segment as BoundSegment)
from hypothesis.searchstrategy import SearchStrategy

from martinez.bounding_box import BoundingBox as PortedBoundingBox
from martinez.contour import Contour as PortedContour
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from martinez.segment import Segment as PortedSegment

Strategy = SearchStrategy
BoundPointsPair = Tuple[BoundPoint, BoundPoint]
BoundPointsTriplet = Tuple[BoundPoint, BoundPoint, BoundPoint]
PortedPointsPair = Tuple[PortedPoint, PortedPoint]
PortedPointsTriplet = Tuple[PortedPoint, PortedPoint, PortedPoint]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


FirstCoordinate = TypeVar('FirstCoordinate')
SecondCoordinate = TypeVar('SecondCoordinate')


def transpose(sequence: Sequence[Tuple[FirstCoordinate, SecondCoordinate]]
              ) -> Tuple[Sequence[FirstCoordinate],
                         Sequence[SecondCoordinate]]:
    sequence_type = type(sequence)
    if not sequence:
        return sequence_type(), sequence_type()
    return tuple(map(sequence_type, zip(*sequence)))


def capacity(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def all_unique(iterable: Iterable[Hashable]) -> bool:
    seen = set()
    for element in iterable:
        if element not in seen:
            seen.add(element)
        else:
            return False
    return True


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


def are_bound_ported_points_sequences_equal(
        bound_points: Sequence[BoundPoint],
        ported_points: Sequence[PortedPoint]) -> bool:
    return (len(bound_points) == len(ported_points)
            and all(map(are_bound_ported_points_equal,
                        bound_points, ported_points)))


def are_bound_ported_segments_equal(bound_segment: BoundSegment,
                                    ported_segment: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound_segment.source,
                                          ported_segment.source)
            and are_bound_ported_points_equal(bound_segment.target,
                                              ported_segment.target))


def is_bounding_box_empty(bounding_box: Union[BoundBoundingBox,
                                              PortedBoundingBox]) -> bool:
    return not (bounding_box.x_min or bounding_box.y_min
                or bounding_box.x_max or bounding_box.y_max)


def are_bound_ported_contours_equal(bound: BoundContour,
                                    ported: PortedContour) -> bool:
    return (are_bound_ported_points_sequences_equal(bound.points,
                                                    ported.points)
            and bound.holes == ported.holes
            and bound.is_external is ported.is_external)


def are_bound_ported_polygons_equal(bound: BoundPolygon,
                                    ported: PortedPolygon) -> bool:
    return all(map(are_bound_ported_contours_equal,
                   bound.contours, ported.contours))


Domain = TypeVar('Domain')


def permute(sequence: Sequence[Domain],
            permutation: Sequence[int]) -> Iterable[Domain]:
    return map(sequence.__getitem__, permutation)


def is_even_permutation(permutation: Sequence[int]) -> bool:
    counter = 0
    for index in range(len(permutation)):
        for next_index in range(index + 1, len(permutation)):
            if permutation[index] > permutation[next_index]:
                counter += 1
    return not counter % 2
