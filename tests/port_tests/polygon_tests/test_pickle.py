from hypothesis import given

from martinez.polygon import Polygon
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.polygons)
def test_round_trip(polygon: Polygon) -> None:
    assert pickle_round_trip(polygon) == polygon
