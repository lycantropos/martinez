from typing import Tuple

from _martinez import BoundingBox as Bound
from hypothesis import given

from martinez.bounding_box import BoundingBox as Ported
from . import strategies


@given(strategies.bound_with_ported_bounding_boxes_pairs,
       strategies.bound_with_ported_bounding_boxes_pairs)
def test_basic(first_bound_with_ported_boxes_pair: Tuple[Bound, Ported],
               second_bound_with_ported_boxes_pair: Tuple[Bound, Ported]
               ) -> None:
    first_bound, first_ported = first_bound_with_ported_boxes_pair
    second_bound, second_ported = second_bound_with_ported_boxes_pair

    bound_result = first_bound + second_bound
    ported_result = first_ported + second_ported

    assert bound_result.x_min == ported_result.x_min
    assert bound_result.y_min == ported_result.y_min
    assert bound_result.x_max == ported_result.x_max
    assert bound_result.y_max == ported_result.y_max
