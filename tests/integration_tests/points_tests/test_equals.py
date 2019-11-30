from _martinez import Point_2
from hypothesis import given

from martinez.point import Point
from tests import strategies
from tests.utils import (equivalence,
                         implication)


@given(strategies.floats, strategies.floats)
def test_reflexivity(x: float, y: float) -> None:
    source, target = Point_2(x, y), Point(x, y)

    assert equivalence(source == source, target == target)


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_symmetry(first_x: float, first_y: float,
                  second_x: float, second_y: float) -> None:
    first_source, second_source = (Point_2(first_x, first_y),
                                   Point_2(second_x, second_y))
    first_target, second_target = (Point(first_x, first_y),
                                   Point(second_x, second_y))

    assert equivalence(equivalence(first_source == second_source,
                                   second_source == first_source),
                       equivalence(first_target == second_target,
                                   second_target == first_target))


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_transitivity(first_x: float, first_y: float,
                      second_x: float, second_y: float,
                      third_x: float, third_y: float) -> None:
    first_source, second_source, third_source = (Point_2(first_x, first_y),
                                                 Point_2(second_x, second_y),
                                                 Point_2(third_x, third_y))
    first_target, second_target, third_target = (Point(first_x, first_y),
                                                 Point(second_x, second_y),
                                                 Point(third_x, third_y))

    assert equivalence(implication(first_source == second_source
                                   and second_source == third_source,
                                   first_source == third_source),
                       implication(first_target == second_target
                                   and second_target == third_target,
                                   first_target == third_target))


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_connection_with_inequality(first_x: float, first_y: float,
                                    second_x: float, second_y: float) -> None:
    first_source, second_source = (Point_2(first_x, first_y),
                                   Point_2(second_x, second_y))
    first_target, second_target = (Point(first_x, first_y),
                                   Point(second_x, second_y))

    assert equivalence(equivalence(not first_source == second_source,
                                   first_source != second_source),
                       equivalence(not first_target == second_target,
                                   first_target != second_target))
