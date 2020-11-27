from hypothesis import given

from tests.bind_tests.hints import BoundPolygon as BoundPolygon
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.polygons)
def test_round_trip(polygon: BoundPolygon) -> None:
    assert pickle_round_trip(polygon) == polygon
