from typing import Tuple

from hypothesis import given

from martinez.point import Point
from tests.utils import equivalence
from . import strategies


@given(strategies.points)
def test_self(point: Point) -> None:
    assert not point.distance_to(point)


@given(strategies.points_pairs)
def test_sign(points_pair: Tuple[Point, Point]) -> None:
    first_point, second_point = points_pair

    assert equivalence(first_point != second_point,
                       first_point.distance_to(second_point) > 0)


@given(strategies.points_pairs)
def test_symmetry(points_pair: Tuple[Point, Point]) -> None:
    first_point, second_point = points_pair

    assert (first_point.distance_to(second_point)
            == second_point.distance_to(first_point))


@given(strategies.points_triplets)
def test_triangle_inequality(points_triplet: Tuple[Point, Point, Point]
                             ) -> None:
    first_point, second_point, third_point = points_triplet

    assert (first_point.distance_to(second_point)
            <= (first_point.distance_to(third_point)
                + third_point.distance_to(second_point)))
