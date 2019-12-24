from typing import Tuple

from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from tests.utils import (are_bound_ported_points_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.points_pairs)
def test_round_trip(points_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = points_pair

    assert are_bound_ported_points_equal(pickle_round_trip(bound),
                                         pickle_round_trip(ported))
