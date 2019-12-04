from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from tests.utils import are_bound_ported_contours_equal
from . import strategies


@given(strategies.bound_with_ported_contours_pairs)
def test_basic(bound_with_ported_contours_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bound_with_ported_contours_pair

    bound.clear_holes()
    ported.clear_holes()

    assert are_bound_ported_contours_equal(bound, ported)
