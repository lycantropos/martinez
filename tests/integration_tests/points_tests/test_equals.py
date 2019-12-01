from typing import Tuple

from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.bounded_with_ported_points_pairs,
       strategies.bounded_with_ported_points_pairs)
def test_basic(first_bounded_with_ported_points_pair: Tuple[Bound, Ported],
               second_bounded_with_ported_points_pair: Tuple[Bound, Ported]
               ) -> None:
    first_bound, first_ported = first_bounded_with_ported_points_pair
    second_bound, second_ported = second_bounded_with_ported_points_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
