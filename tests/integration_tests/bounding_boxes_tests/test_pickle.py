from typing import Tuple

from _martinez import BoundingBox as Bound
from hypothesis import given

from martinez.bounding_box import BoundingBox as Ported
from tests.utils import (are_bound_ported_bounding_boxes_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.bounding_boxes_pairs)
def test_round_trip(bounding_boxes_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(pickle_round_trip(bound),
                                                 pickle_round_trip(ported))
