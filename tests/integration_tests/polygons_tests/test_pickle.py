from typing import Tuple

from _martinez import Polygon as Bound
from hypothesis import given

from martinez.polygon import Polygon as Ported
from tests.utils import (pickle_round_trip)
from ..utils import are_bound_ported_polygons_equal
from . import strategies


@given(strategies.polygons_pairs)
def test_round_trip(polygons_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = polygons_pair

    assert are_bound_ported_polygons_equal(pickle_round_trip(bound),
                                           pickle_round_trip(ported))
