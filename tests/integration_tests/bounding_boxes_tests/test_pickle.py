from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from tests.integration_tests.utils import are_bound_ported_bounding_boxes_equal
from tests.port_tests.hints import PortedBoundingBox
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.bounding_boxes_pairs)
def test_round_trip(bounding_boxes_pair: Tuple[BoundBoundingBox,
                                               PortedBoundingBox]) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(pickle_round_trip(bound),
                                                 pickle_round_trip(ported))
