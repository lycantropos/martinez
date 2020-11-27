from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.integration_tests.utils import are_bound_ported_contours_equal
from tests.port_tests.hints import PortedContour
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.contours_pairs)
def test_round_trip(contours_pair: Tuple[BoundContour, PortedContour]) -> None:
    bound, ported = contours_pair

    assert are_bound_ported_contours_equal(pickle_round_trip(bound),
                                           pickle_round_trip(ported))
