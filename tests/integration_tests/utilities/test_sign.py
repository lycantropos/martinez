from typing import Tuple

from _martinez import sign as bound_sign
from hypothesis import given

from martinez.utilities import sign as ported_sign
from tests.utils import (BoundPointsTriplet,
                         PortedPointsTriplet)
from . import strategies


@given(strategies.bound_with_ported_points_triplets_pairs)
def test_basic(
        bound_with_ported_points_triplets_pair: Tuple[PortedPointsTriplet,
                                                      BoundPointsTriplet]
) -> None:
    bound_points, ported_points = bound_with_ported_points_triplets_pair

    assert bound_sign(*bound_points) == ported_sign(*ported_points)
