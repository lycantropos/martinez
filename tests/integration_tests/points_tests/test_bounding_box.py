from typing import Tuple

from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from ..utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = points_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
