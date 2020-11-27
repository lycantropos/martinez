from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from tests.integration_tests.utils import are_bound_ported_polygons_equal
from tests.port_tests.hints import PortedPolygon
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.polygons_pairs)
def test_round_trip(polygons_pair: Tuple[BoundPolygon, PortedPolygon]) -> None:
    bound, ported = polygons_pair

    assert are_bound_ported_polygons_equal(pickle_round_trip(bound),
                                           pickle_round_trip(ported))
