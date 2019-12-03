from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from . import strategies


@given(strategies.bound_with_ported_contours_pairs)
def test_basic(bound_with_ported_contours_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bound_with_ported_contours_pair

    assert bound.is_counterclockwise is ported.is_counterclockwise