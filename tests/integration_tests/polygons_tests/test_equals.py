from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from tests.port_tests.hints import PortedPolygon
from tests.utils import equivalence
from . import strategies


@given(strategies.polygons_pairs, strategies.polygons_pairs)
def test_basic(first_polygons_pair: Tuple[BoundPolygon, PortedPolygon],
               second_polygons_pair: Tuple[BoundPolygon, PortedPolygon]
               ) -> None:
    first_bound, first_ported = first_polygons_pair
    second_bound, second_ported = second_polygons_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
