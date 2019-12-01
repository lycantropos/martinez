from typing import Tuple

from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.bounded_with_ported_points_pairs)
def test_reflexivity(bounded_with_ported_points_pair: Tuple[Bound, Ported]
                     ) -> None:
    bound, ported = bounded_with_ported_points_pair

    assert equivalence(bound == bound, ported == ported)


@given(strategies.bounded_with_ported_points_pairs,
       strategies.bounded_with_ported_points_pairs)
def test_symmetry(first_bounded_with_ported_points_pair: Tuple[Bound, Ported],
                  second_bounded_with_ported_points_pair: Tuple[Bound, Ported]
                  ) -> None:
    first_bound, first_ported = first_bounded_with_ported_points_pair
    second_bound, second_ported = second_bounded_with_ported_points_pair

    assert equivalence(equivalence(first_bound == second_bound,
                                   second_bound == first_bound),
                       equivalence(first_ported == second_ported,
                                   second_ported == first_ported))


@given(strategies.bounded_with_ported_points_pairs,
       strategies.bounded_with_ported_points_pairs,
       strategies.bounded_with_ported_points_pairs)
def test_transitivity(
        first_bounded_with_ported_points_pair: Tuple[Bound, Ported],
        second_bounded_with_ported_points_pair: Tuple[Bound, Ported],
        third_bounded_with_ported_points_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_bounded_with_ported_points_pair
    second_bound, second_ported = second_bounded_with_ported_points_pair
    third_bound, third_ported = third_bounded_with_ported_points_pair

    assert equivalence(implication(first_bound == second_bound
                                   and second_bound == third_bound,
                                   first_bound == third_bound),
                       implication(first_ported == second_ported
                                   and second_ported == third_ported,
                                   first_ported == third_ported))


@given(strategies.bounded_with_ported_points_pairs,
       strategies.bounded_with_ported_points_pairs)
def test_connection_with_inequality(
        first_bounded_with_ported_points_pair: Tuple[Bound, Ported],
        second_bounded_with_ported_points_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_bounded_with_ported_points_pair
    second_bound, second_ported = second_bounded_with_ported_points_pair

    assert equivalence(equivalence(not first_bound == second_bound,
                                   first_bound != second_bound),
                       equivalence(not first_ported == second_ported,
                                   first_ported != second_ported))
