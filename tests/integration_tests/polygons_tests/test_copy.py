import copy
from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundPolygon
from tests.integration_tests.utils import are_bound_ported_polygons_equal
from tests.port_tests.hints import PortedPolygon
from . import strategies


@given(strategies.polygons_pairs)
def test_shallow(polygons_pair: Tuple[BoundPolygon, PortedPolygon]) -> None:
    bound, ported = polygons_pair

    assert are_bound_ported_polygons_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.polygons_pairs)
def test_deep(polygons_pair: Tuple[BoundPolygon, PortedPolygon]) -> None:
    bound, ported = polygons_pair

    assert are_bound_ported_polygons_equal(copy.deepcopy(bound),
                                           copy.deepcopy(ported))
