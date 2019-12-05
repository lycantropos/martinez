from typing import Tuple

from _martinez import Polygon as Bound
from hypothesis import given

from martinez.polygon import Polygon as Ported
from tests.utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.bound_with_ported_polygons_pairs)
def test_basic(bound_with_ported_polygons_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bound_with_ported_polygons_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
