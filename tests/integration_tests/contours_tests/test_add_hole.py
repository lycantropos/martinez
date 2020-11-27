from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from ..utils import are_bound_ported_contours_equal
from . import strategies


@given(strategies.contours_pairs, strategies.non_negative_integers)
def test_basic(contours_pair: Tuple[Bound, Ported],
               hole: int) -> None:
    bound, ported = contours_pair

    bound.add_hole(hole)
    ported.add_hole(hole)

    assert are_bound_ported_contours_equal(bound, ported)
