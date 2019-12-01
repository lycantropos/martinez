import math

from _martinez import Point
from hypothesis import given

from tests.utils import equivalence
from . import strategies


@given(strategies.points)
def test_self(point: Point) -> None:
    assert not point.distance_to(point)


@given(strategies.points, strategies.points)
def test_sign(first_point: Point, second_point: Point) -> None:
    assert equivalence(first_point != second_point,
                       first_point.distance_to(second_point) > 0)


@given(strategies.points, strategies.points)
def test_symmetry(first_point: Point, second_point: Point) -> None:
    assert (first_point.distance_to(second_point)
            == second_point.distance_to(first_point))


@given(strategies.points, strategies.points, strategies.points)
def test_triangle_inequality(first_point: Point,
                             second_point: Point,
                             third_point: Point) -> None:
    straight_distance = first_point.distance_to(second_point)
    workaround_distance = (first_point.distance_to(third_point)
                           + third_point.distance_to(second_point))

    assert (straight_distance <= workaround_distance
            or math.isclose(straight_distance, workaround_distance))
