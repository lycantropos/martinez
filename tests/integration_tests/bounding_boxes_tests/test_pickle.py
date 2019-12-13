import pickle
from typing import Tuple

from _martinez import BoundingBox as Bound
from hypothesis import given

from martinez.bounding_box import BoundingBox as Ported
from tests.utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.bound_with_ported_bounding_boxes_pairs)
def test_round_trip(bound_with_ported_bounding_boxes_pair: Tuple[Bound, Ported]
                    ) -> None:
    bound, ported = bound_with_ported_bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(
            pickle.loads(pickle.dumps(bound)),
            pickle.loads(pickle.dumps(ported)))
