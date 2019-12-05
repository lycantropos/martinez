import pickle

from _martinez import Polygon
from hypothesis import given

from . import strategies


@given(strategies.polygons)
def test_round_trip(polygon: Polygon) -> None:
    assert pickle.loads(pickle.dumps(polygon)) == polygon
