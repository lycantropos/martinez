from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from . import strategies


@given(strategies.contours_pairs)
def test_basic(contours_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = contours_pair

    assert bound.is_clockwise is ported.is_clockwise
