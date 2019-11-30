from typing import Any

from hypothesis import given

from martinez.point import Point
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.points)
def test_reflexivity(point: Point) -> None:
    assert point == point


@given(strategies.points, strategies.points)
def test_symmetry(first_point: Point,
                  second_point: Point) -> None:
    assert equivalence(first_point == second_point,
                       second_point == first_point)


@given(strategies.points, strategies.points, strategies.points)
def test_transitivity(first_point: Point, second_point: Point,
                      third_point: Point) -> None:
    assert implication(first_point == second_point
                       and second_point == third_point,
                       first_point == third_point)


@given(strategies.points, strategies.points)
def test_connection_with_inequality(first_point: Point,
                                    second_point: Point) -> None:
    assert equivalence(not first_point == second_point,
                       first_point != second_point)


@given(strategies.points, strategies.non_points)
def test_non_point(point: Point, non_point: Any) -> None:
    assert point != non_point
