from itertools import permutations

from hypothesis import given

from martinez.utilities import sign
from tests.port_tests.hints import PortedPointsTriplet
from tests.utils import (is_even_permutation,
                         permute)
from . import strategies


@given(strategies.points_triplets)
def test_basic(points_triplet: PortedPointsTriplet) -> None:
    first_point, second_point, third_point = points_triplet

    result = sign(first_point, second_point, third_point)

    assert result in {-1, 0, 1}


@given(strategies.points_triplets)
def test_permutations(points_triplet: PortedPointsTriplet) -> None:
    first_point, second_point, third_point = points_triplet

    result = sign(first_point, second_point, third_point)

    points = [first_point, second_point, third_point]
    assert all(sign(*permute(points, permutation)) ==
               (result if is_even_permutation(permutation) else -result)
               for permutation in permutations(range(3)))
