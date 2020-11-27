from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPoint
from tests.port_tests.hints import PortedPoint
from tests.utils import equivalence
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(first_points_pair: Tuple[BoundPoint, PortedPoint],
               second_points_pair: Tuple[BoundPoint, PortedPoint]
               ) -> None:
    first_bound, first_ported = first_points_pair
    second_bound, second_ported = second_points_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
