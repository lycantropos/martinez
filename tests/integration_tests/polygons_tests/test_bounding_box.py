from typing import Tuple

from _martinez import Polygon as Bound
from hypothesis import given

from martinez.polygon import Polygon as Ported
from tests.utils import are_bound_ported_bounding_boxes_equal
from . import strategies


@given(strategies.polygons_pairs)
def test_basic(polygons_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = polygons_pair

    assert are_bound_ported_bounding_boxes_equal(bound.bounding_box,
                                                 ported.bounding_box)
