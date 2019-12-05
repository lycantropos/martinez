import pickle

from hypothesis import given

from martinez.polygon import Polygon
from . import strategies


@given(strategies.polygons)
def test_round_trip(polygon: Polygon) -> None:
    assert pickle.loads(pickle.dumps(polygon)) == polygon
