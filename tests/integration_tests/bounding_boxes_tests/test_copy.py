import copy
from typing import Tuple

from _martinez import BoundingBox as Bound
from hypothesis import given

from martinez.bounding_box import BoundingBox as Ported
from tests.utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.bound_with_ported_bounding_boxes_pairs)
def test_shallow(bound_with_ported_bounding_boxes_pair: Tuple[Bound, Ported]
                 ) -> None:
    bound, ported = bound_with_ported_bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(copy.copy(bound),
                                                 copy.copy(ported))


@given(strategies.bound_with_ported_bounding_boxes_pairs)
def test_deep(bound_with_ported_bounding_boxes_pair: Tuple[Bound, Ported]
              ) -> None:
    bound, ported = bound_with_ported_bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(copy.deepcopy(bound),
                                                 copy.deepcopy(ported))
