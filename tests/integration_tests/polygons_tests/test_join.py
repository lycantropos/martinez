from typing import Tuple

from _martinez import Polygon as Bound
from hypothesis import given

from martinez.polygon import Polygon as Ported
from ..utils import are_bound_ported_polygons_equal
from . import strategies


@given(strategies.polygons_pairs, strategies.polygons_pairs)
def test_basic(first_polygons_pair: Tuple[Bound, Ported],
               second_polygons_pair: Tuple[Bound, Ported]) -> None:
    first_bound, first_ported = first_polygons_pair
    second_bound, second_ported = second_polygons_pair

    assert are_bound_ported_polygons_equal(first_bound, first_ported)

    first_bound.join(second_bound)
    first_ported.join(second_ported)

    assert are_bound_ported_polygons_equal(first_bound, first_ported)
    assert are_bound_ported_polygons_equal(second_bound, second_ported)
