import copy
from typing import Tuple

from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from tests.utils import are_bound_ported_points_equal
from . import strategies


@given(strategies.bound_with_ported_points_pairs)
def test_shallow(bound_with_ported_points_pair: Tuple[Bound, Ported]
                 ) -> None:
    bound, ported = bound_with_ported_points_pair

    assert are_bound_ported_points_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.bound_with_ported_points_pairs)
def test_deep(bound_with_ported_points_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bound_with_ported_points_pair

    assert are_bound_ported_points_equal(copy.deepcopy(bound),
                                         copy.deepcopy(ported))
