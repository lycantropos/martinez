from hypothesis import given

from tests.port_tests.hints import PortedPolygon
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.polygons)
def test_round_trip(polygon: PortedPolygon) -> None:
    assert pickle_round_trip(polygon) == polygon
