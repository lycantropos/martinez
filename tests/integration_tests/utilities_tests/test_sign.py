from typing import Tuple

from _martinez import sign as bound_sign
from hypothesis import given

from martinez.utilities import sign as ported_sign
from ...port_tests.utils import PortedPointsTriplet
from ...bind_tests.utils import BoundPointsTriplet
from . import strategies


@given(strategies.points_triplets_pairs)
def test_basic(points_triplets_pair: Tuple[PortedPointsTriplet,
                                           BoundPointsTriplet]) -> None:
    bound_points, ported_points = points_triplets_pair

    assert bound_sign(*bound_points) == ported_sign(*ported_points)
