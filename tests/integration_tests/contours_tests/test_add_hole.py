from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.integration_tests.utils import are_bound_ported_contours_equal
from tests.port_tests.hints import PortedContour
from . import strategies


@given(strategies.contours_pairs, strategies.non_negative_integers)
def test_basic(contours_pair: Tuple[BoundContour, PortedContour],
               hole: int) -> None:
    bound, ported = contours_pair

    bound.add_hole(hole)
    ported.add_hole(hole)

    assert are_bound_ported_contours_equal(bound, ported)
