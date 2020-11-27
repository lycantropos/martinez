import copy
from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from tests.integration_tests.utils import are_bound_ported_bounding_boxes_equal
from tests.port_tests.hints import PortedBoundingBox
from . import strategies


@given(strategies.bounding_boxes_pairs)
def test_shallow(bounding_boxes_pair: Tuple[BoundBoundingBox,
                                            PortedBoundingBox]) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(copy.copy(bound),
                                                 copy.copy(ported))


@given(strategies.bounding_boxes_pairs)
def test_deep(bounding_boxes_pair: Tuple[BoundBoundingBox,
                                         PortedBoundingBox]) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(copy.deepcopy(bound),
                                                 copy.deepcopy(ported))
