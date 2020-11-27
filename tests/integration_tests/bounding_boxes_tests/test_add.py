from typing import Tuple

from _martinez import BoundingBox as Bound
from hypothesis import given

from martinez.bounding_box import BoundingBox as Ported
from ..utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.bounding_boxes_pairs, strategies.bounding_boxes_pairs)
def test_basic(first_bounding_boxes_pair: Tuple[Bound, Ported],
               second_bounding_boxes_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_bounding_boxes_pair
    second_bound, second_ported = second_bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(first_bound + second_bound,
                                                 first_ported + second_ported)
