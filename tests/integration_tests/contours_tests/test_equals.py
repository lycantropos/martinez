from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.port_tests.hints import PortedContour
from tests.utils import equivalence
from . import strategies


@given(strategies.contours_pairs, strategies.contours_pairs)
def test_basic(first_contours_pair: Tuple[BoundContour, PortedContour],
               second_contours_pair: Tuple[BoundContour, PortedContour]
               ) -> None:
    first_bound, first_ported = first_contours_pair
    second_bound, second_ported = second_contours_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
