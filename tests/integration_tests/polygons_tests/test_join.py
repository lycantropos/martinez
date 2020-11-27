from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from tests.integration_tests.utils import are_bound_ported_polygons_equal
from tests.port_tests.hints import PortedPolygon
from . import strategies


@given(strategies.polygons_pairs, strategies.polygons_pairs)
def test_basic(first_polygons_pair: Tuple[BoundPolygon, PortedPolygon],
               second_polygons_pair: Tuple[
                   BoundPolygon, PortedPolygon]) -> None:
    first_bound, first_ported = first_polygons_pair
    second_bound, second_ported = second_polygons_pair

    assert are_bound_ported_polygons_equal(first_bound, first_ported)

    first_bound.join(second_bound)
    first_ported.join(second_ported)

    assert are_bound_ported_polygons_equal(first_bound, first_ported)
    assert are_bound_ported_polygons_equal(second_bound, second_ported)
