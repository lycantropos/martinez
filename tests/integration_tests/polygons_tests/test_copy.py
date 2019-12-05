import copy
from typing import Tuple

from _martinez import Polygon as Bound
from hypothesis import given

from martinez.polygon import Polygon as Ported
from tests.utils import are_bound_ported_polygons_equal
from . import strategies


@given(strategies.bound_with_ported_polygons_pairs)
def test_shallow(bound_with_ported_polygons_pair: Tuple[Bound, Ported]
                 ) -> None:
    bound, ported = bound_with_ported_polygons_pair

    assert are_bound_ported_polygons_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.bound_with_ported_polygons_pairs)
def test_deep(bound_with_ported_polygons_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = bound_with_ported_polygons_pair

    assert are_bound_ported_polygons_equal(copy.deepcopy(bound),
                                           copy.deepcopy(ported))
