from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPoint
from tests.integration_tests.utils import are_bound_ported_points_equal
from tests.port_tests.hints import PortedPoint
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.points_pairs)
def test_round_trip(points_pair: Tuple[BoundPoint, PortedPoint]) -> None:
    bound, ported = points_pair

    assert are_bound_ported_points_equal(pickle_round_trip(bound),
                                         pickle_round_trip(ported))
