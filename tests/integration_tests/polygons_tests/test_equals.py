from typing import Tuple

from _martinez import Polygon as Bound
from hypothesis import given

from martinez.polygon import Polygon as Ported
from tests.utils import equivalence
from . import strategies


@given(strategies.bound_with_ported_polygons_pairs,
       strategies.bound_with_ported_polygons_pairs)
def test_basic(first_bound_with_ported_polygons_pair: Tuple[Bound, Ported],
               second_bound_with_ported_polygons_pair: Tuple[Bound, Ported]
               ) -> None:
    first_bound, first_ported = first_bound_with_ported_polygons_pair
    second_bound, second_ported = second_bound_with_ported_polygons_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
