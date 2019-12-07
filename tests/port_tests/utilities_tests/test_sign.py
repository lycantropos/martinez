from itertools import permutations
from typing import Tuple

from hypothesis import given

from martinez.point import Point
from martinez.utilities import sign
from tests.utils import (equivalence,
                         is_even_permutation,
                         permute)
from . import strategies


@given(strategies.points_triplets)
def test_basic(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_point, second_point, third_point = points_triplet

    result = sign(first_point, second_point, third_point)

    assert result in {-1, 0, 1}


@given(strategies.points_triplets)
def test_permutations(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_point, second_point, third_point = points_triplet

    result = sign(first_point, second_point, third_point)

    points = [first_point, second_point, third_point]
    assert (all(sign(*points) == result
                for points in permutations(points))
            if result == 0
            else all(equivalence(is_even_permutation(permutation),
                                 sign(*permute(points, permutation)) == result)
                     for permutation in permutations(range(3))))
