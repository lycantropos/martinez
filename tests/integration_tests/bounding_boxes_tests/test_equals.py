from typing import Tuple

from _martinez import BoundingBox as BoundBoundingBox
from hypothesis import given

from martinez.bounding_box import BoundingBox as PortedBoundingBox
from tests.utils import equivalence
from . import strategies


@given(strategies.bounding_boxes_pairs, strategies.bounding_boxes_pairs)
def test_basic(first_bounding_boxes_pair: Tuple[BoundBoundingBox, PortedBoundingBox],
               second_bounding_boxes_pair: Tuple[BoundBoundingBox, PortedBoundingBox]) -> None:
    first_bound, first_ported = first_bounding_boxes_pair
    second_bound, second_ported = second_bounding_boxes_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
