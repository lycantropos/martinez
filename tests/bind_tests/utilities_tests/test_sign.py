from itertools import permutations

from _martinez import (Point,
                       sign)
from hypothesis import given

from tests.utils import (equivalence,
                         is_even_permutation,
                         permute)
from . import strategies


@given(strategies.points, strategies.points, strategies.points)
def test_basic(first_point: Point,
               second_point: Point,
               third_point: Point) -> None:
    result = sign(first_point, second_point, third_point)

    assert result in {-1, 0, 1}


@given(strategies.points, strategies.points, strategies.points)
def test_permutations(first_point: Point,
                      second_point: Point,
                      third_point: Point) -> None:
    result = sign(first_point, second_point, third_point)

    points = [first_point, second_point, third_point]
    assert (all(sign(*points) == result
                for points in permutations(points))
            if result == 0
            else all(equivalence(is_even_permutation(permutation),
                                 sign(*permute(points, permutation)) == result)
                     for permutation in permutations(range(3))))
