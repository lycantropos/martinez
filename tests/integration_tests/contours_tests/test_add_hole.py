from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from . import strategies


@given(strategies.bound_with_ported_contours_pairs,
       strategies.non_negative_integers)
def test_basic(bound_with_ported_contours_pair: Tuple[Bound, Ported],
               hole: int) -> None:
    bound, ported = bound_with_ported_contours_pair

    bound.add_hole(hole)
    ported.add_hole(hole)

    assert bound.holes[-1] == ported.holes[-1]
