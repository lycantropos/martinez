from typing import Tuple

from _martinez import Contour as Bound
from hypothesis import given

from martinez.contour import Contour as Ported
from ..utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.contours_pairs)
def test_basic(contours_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = contours_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
